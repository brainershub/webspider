# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class CsiroSpider(scrapy.Spider):
    name = 'csiro'
    allowed_domains = ['www.publish.csiro.au']
    start_urls = ['https://www.publish.csiro.au/journals/all']

    title_xpath = '//h1/text()'
    text_xpath = '//h2[text()="Abstract"]/parent::div/descendant::text()'
    author_xpath = '//*[@class="editors"]/text() | //*[@class="Editors"]/text()'
    contentdate_xpath = 'substring-after(//div[@class="Journal_editors"]/p/text()[last()-1], "Published:")'

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

    def parse(self, response):
        journals = response.xpath('//div[@id="hero-image"]/following-sibling::div//a')
        for j in journals:
            yield response.follow(url=j, callback=self.extract_journal)


    def extract_journal(self, response):
        yield SplashRequest(url=response.url, callback=self.parse_journal, endpoint='execute', args={
                'lua_source': self.script
            })
        
    def parse_journal(self, response):
        articles = response.xpath('//a[text()=" Abstract"]')
        for a in articles:
            yield response.follow(url=a, callback=self.parse_page)

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
