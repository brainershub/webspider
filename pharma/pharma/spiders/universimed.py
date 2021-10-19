import scrapy
from scrapy_splash import SplashRequest


class UniversimedSpider(scrapy.Spider):
    name = 'universimed'
    allowed_domains = ['www.universimed.com']
    start_urls = ['https://www.universimed.com/de/fachthemen']

    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'

    title_xpath = '//h1/text()'
    text_xpath = '//div[@class="csArticle-page_main"]//p/descendant::text()'
    author_xpath = '//p[contains(text(),"Autor")]/following-sibling::p/b/text()'
    contentdate_xpath = '//span[@class="date title"]/text()'

    script = '''
    function main(splash, args)
        splash.private_mode_enabled = false
        url = args.url
        assert(splash:go(url))
        assert(splash:wait(1))
        local element = splash:select('.load-more_btn')
        local bounds = element:bounds()
        assert(element:mouse_click{x=bounds.width/2, y=bounds.height/2})
        assert(splash:wait(2))
        local element = splash:select('.load-more_btn')
        local bounds = element:bounds()
        assert(element:mouse_click{x=bounds.width/2, y=bounds.height/2})
        assert(splash:wait(2))
        splash:set_viewport_full()
        return splash:html()
    end
    '''

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={
                'lua_source': self.script
            })


    def parse(self, response):
        links = response.xpath('//a[contains(text(), "Zum Artikel")]/@href').getall()
        for link in links:
            yield response.follow(url=link, callback=self.parse_article)

        
    def parse_article(self, response):  
        author_list = response.xpath(self.author_xpath).getall()
        authors = ', '.join(author_list)

        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)

        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': authors,
            'content_text': text,
            'content_date': response.xpath(self.contentdate_xpath).get(),
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }
