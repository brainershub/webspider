# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class ContraceptionSpider(CrawlSpider):
    name = 'contraception'
    allowed_domains = ['contraceptionmedicine.biomedcentral.com']
    start_urls = ['https://contraceptionmedicine.biomedcentral.com/articles']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[@data-test="title-link"]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[@rel="next"]'), callback='parse_item', follow=True),
    )

    title_xpath = '//h1/text()'
    text_xpath = '//div[@id="Abs1-content"]/p/descendant::text() | //div[@id="Abs1-content"]/h3/text()'
    author_xpath = '//a[@data-test="author-name"]/text()'
    contentdate_xpath = '//article//li/a/time/text()'


    def parse_item(self, response):
        author_list = response.xpath(self.author_xpath).getall()
        # if author_list:
        #     authors = author_list
        # else:
        #     authors = 'None'
        authors = ', '.join(author_list)
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

