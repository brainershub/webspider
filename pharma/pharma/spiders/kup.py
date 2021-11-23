# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime


class KupSpider(scrapy.Spider):
    name = 'kup'
    allowed_domains = ['www.kup.at']
    start_urls = ['https://www.kup.at/journals/reproduktionsmedizin']
    
    title_xpath = '//div[@class="summarybox-content"]/b[1]/text()'
    text_xpath = '//p[@class="PR-Flie--"]/descendant::text()'

    def parse(self, response):
        links = response.xpath('//a[text()="Volltext (HTML)"]')
        for l in links:
            yield response.follow(url=l, callback=self.parse_page)

    

    def parse_page(self, response):
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)

        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': 'KUP',
            'content_text': text,
            'content_date': datetime.utcnow(),
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }