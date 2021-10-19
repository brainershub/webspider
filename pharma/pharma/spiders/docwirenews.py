# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class DocwirenewsSpider(scrapy.Spider):
    name = 'docwirenews'
    allowed_domains = ['www.docwirenews.com']
    start_urls = ['https://www.docwirenews.com/category/docwire-pick']

    title_xpath = '//h1/text()'
    text_xpath = '//div[@class="td-post-content"]/descendant::text()'
    author_xpath = '//div[@class="td-post-author-name"]/a/text()'
    contentdate_xpath = '//article//time[contains(@class, "entry-date")]/text()'

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
        links = response.xpath('//h3/a')
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
            'labels': 'news'
        }
