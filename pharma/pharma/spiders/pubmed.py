import scrapy
from scrapy_splash import SplashRequest


class PubmedSpider(scrapy.Spider):
    name = 'pubmed'
    allowed_domains = ['pubmed.ncbi.nlm.nih.gov']
    start_urls = ['https://pubmed.ncbi.nlm.nih.gov/trending']

    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'

    title_xpath = '//h1/text()'
    text_xpath = '//div[@id="article-abstract-content1"]/descendant::text() | //section[@id="ArticleBody"]/descendant::text()'
    author_xpath = '//section[@id="ejp-article-authors"]/p/text()'
    contentdate_xpath = 'substring-after(//p[contains(text(), "Published online")]/text(), "Published online")'

    script = '''
    function main(splash, args)
    assert(splash:go(args.url))
    assert(splash:wait(0.5))
    counter = 3
    local get_dimensions = splash:jsfunc([[ 
            function (selector) {
                var rect = document.querySelector(selector).getClientRects()[0];
                        if (rect) {
                    return {"x": rect.left, "y": rect.top};
                        }
                        else { 
                            return NaN;
                        }
            } 
        ]]) 
    splash:set_viewport_full() 
    splash:wait(0.1)
    while get_dimensions('.load-button.next-page') and counter do
        local dimensions = get_dimensions('.load-button.next-page') 
        splash:mouse_click(dimensions.x, dimensions.y)
        splash:wait(0.1)
        counter = counter - 1
    end
    return {
        html = splash:html(),
    }
    end
    '''

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={
                'lua_source': self.script
            })


    def parse(self, response):
        links = response.xpath('//h4/a/@href').getall()
        for link in links:
            yield response.follow(url=link, callback=self.parse_article, endpoint='execute')
        
    def parse_article(self, response):  
        author_list = response.xpath(self.author_xpath).getall()
        authors = ', '.join(author_list)

        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)

        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': authors,
            'content_text': text,
            'content_date': response.xpath(self.contentdate_xpath),
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }
