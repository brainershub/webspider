import scrapy
from scrapy_splash import SplashRequest


class KargerSpider(scrapy.Spider):
    name = 'karger'
    allowed_domains = ['www.karger.com']
    start_urls = ['https://www.karger.com/search?nR%5BAccess%5D%5B%3D%5D%5B0%5D=2&q=reproductive']

    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'

    title_xpath = '//h1/text()'
    text_xpath = '//div[@id="fulltext"]/descendant::text()'
    author_xpath = '//span[@class="autoren"]/text()'
    contentdate_xpath = 'substring-after(//div[@class="row-fluid" and preceding-sibling::h2]/div[contains(@class, "details")]/p[1]/text()[last()], ": ")'

    script = '''
    function main(splash, args)
        splash.private_mode_enabled = false
        url = args.url
        assert(splash:go(url))
        assert(splash:wait(1))
        splash:set_viewport_full()
        return splash:html()
    end
    '''

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={
                'lua_source': self.script
            })

    # def set_user_agent(self, request):
    #     request.headers['User-Agent'] = self.user_agent
    #     return request

    def parse(self, response):
        links = response.xpath('//h4[@class="media-heading"]/a/@href').getall()
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
