# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class DegruyterSpider(CrawlSpider):
    name = 'degruyter'
    allowed_domains = ['www.degruyter.com']
    start_urls = ['http://www.degruyter.com/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@id="newOpenAccessContainer"]//a[parent::span]'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//a[text()="Next ›"]'), callback='parse_item', follow=True),
    )

    title_xpath = '//h1/text()'
    text_xpath = '//div[@class="article"]//p/descendant::text()'
    author_xpath = '//span[@class="contributor"]/text()'
    contentdate_xpath = '//span[@class="publicationDate"]/text()'


    def parse_item(self, response):
        author_list = response.xpath(self.author_xpath).getall()
        authors = ' '.join(author_list)
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        content_date_raw = response.xpath(self.contentdate_xpath).get()
        content_date_clean = clean_date(content_date_raw)

        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': authors,
            'content_text': text,
            'content_date': content_date_clean,
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }
