# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class PresseportalSpider(scrapy.Spider):
    name = 'presseportal'
    allowed_domains = ['www.presseportal.de']
    start_urls = ['https://www.presseportal.de/t/gesundheit-medizin']


    title_xpath = '//h1/text()'
    text_xpath = '//div[@class="card"]/p[child::text()]/descendant::text()'
    author_xpath = '//a[@class="story-customer"]/text()'
    contentdate_xpath = 'substring-before(//p[@class="date"]/text(), "–")'

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

    def parse(self, response):
        links = response.xpath('//h3[@class="news-headline-clamp"]')
        for link in links:
            yield response.follow(url=link.xpath('./a/@href').get(), callback=self.parse_item, meta={'date': link.xpath('substring-before(./preceding-sibling::div[@class="news-meta"]/h5[@class="date"]/text(), "–")').get()})

    def parse_item(self, response):
        # author_list = response.xpath(self.author_xpath).getall()
        authors = response.xpath(self.author_xpath).get()
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)

        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': authors,
            'content_text': text,
            'content_date': response.meta.get('date'),
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'news'
        }
