# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date
from datetime import datetime


class ImabeSpider(CrawlSpider):
    name = 'imabe'
    allowed_domains = ['www.imabe.org']
    start_urls = ['https://www.imabe.org/bioethikaktuell']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h3/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//li[@class="last next"]/a'), callback='parse_item', follow=True),
    )

    title_xpath = '//h1/text()'
    text_xpath = '//div[@itemprop="articleBody"]/p[child::text()]/descendant::text()'
    author_xpath = '//time/text()'
    contentdate_xpath = '//time/@datetime'


    def parse_item(self, response):
        authors = response.xpath(self.author_xpath).get()
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        content_date_raw = response.xpath(self.contentdate_xpath).get()
        content_date_clean = clean_date(content_date_raw)
        # content_date_clean = datetime.strptime(response.xpath(self.contentdate_xpath).get().strftime("%d-%m-%Y"), '%d-%m-%Y')

        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': authors,
            'content_text': text,
            'content_date': content_date_clean,
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'news'
        }