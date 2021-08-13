import scrapy
from scrapy_splash import SplashRequest


class GelbelisteSpider(scrapy.Spider):
    name = 'gelbeliste'
    allowed_domains = ['www.gelbe-liste.de']
    start_urls = ['http://www.gelbe-liste.de/nachrichten/archiv']

    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'

    title_xpath = '//h1/text()'
    text_xpath = '//div[@class="article"]/descendant::text()'
    author_xpath = '//div[contains(text(), "Stand:")]/preceding-sibling::div/a/text()'
    contentdate_xpath = '//div[contains(text(), "Stand:")]/following-sibling::div/text()'

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
        links = response.xpath('//div[@class="column"]/a')
        for link in links:
            yield response.follow(url=link, callback=self.parse_article)
        
    def parse_article(self, response):    
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': response.xpath(self.author_xpath).get(),
            'text': text,
            'content_date': response.xpath(self.contentdate_xpath).get(),
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'news'
        }
