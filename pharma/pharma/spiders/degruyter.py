# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class DegruyterSpider(CrawlSpider):
    name = 'degruyter'
    allowed_domains = ['www.degruyter.com']
    start_urls = ['https://www.degruyter.com/search?query=*&sortBy=mostrecent&documentTypeFacet=article&publisherFacet=De+Gruyter']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h2[contains(@class, "title")]/parent::a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="pagination"]/li[last()]/a'), follow=True),
    )

    title_xpath = '//h1[not(@class)]/text()'
    text_xpath = '//div[@class="article"]/descendant::text()'
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
