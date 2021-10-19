# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class FrontiersinSpider(scrapy.Spider):
    name = 'frontiersin'
    allowed_domains = ['www.frontiersin.org']
    start_urls = ['https://www.frontiersin.org/journals/physiology#articles']

    title_xpath = '//div[@class="article-section"]//h1/text()'
    text_xpath = '//ul[@class="notes"]/following-sibling::p/descendant::text()'
    author_xpath = '//div[@class="authors"]/a/text()'
    contentdate_xpath = '//*[@id="timestamps"]/text()[last()]'

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
        links = response.xpath('//a[@class="articles-title"]')
        for link in links:
            yield response.follow(url=link, callback=self.parse_page)



    def parse_page(self, response):
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
