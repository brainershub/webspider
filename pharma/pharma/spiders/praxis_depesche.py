# -*- coding: utf-8 -*-
from datetime import date, datetime
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date


class PraxisDepescheSpider(CrawlSpider):
    name = 'praxis-depesche'
    allowed_domains = ['www.praxis-depesche.de']
    start_urls = ['https://www.praxis-depesche.de/nachrichten.html']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h3[not(child::img)]/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//li[@class="navNext"]/a'), callback='parse_item', follow=True),
    )

    title_xpath = '//h1/text()'
    text_xpath = '//div[@class="content"]/descendant::text()'
    author_xpath = '//a[parent::p][1]/text()'
    # contentdate_xpath = 'substring-before(//p[@class="date"]/text(), "–")'


    def parse_item(self, response):
        # author_list = response.xpath(self.author_xpath).getall()
        authors = response.xpath(self.author_xpath).get()
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        # content_date_raw = response.xpath(self.contentdate_xpath).get()
        content_date_clean = datetime.utcnow()

        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': authors,
            'content_text': text,
            'content_date': content_date_clean,
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }
