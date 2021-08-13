# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date


class SaarlandSpider(CrawlSpider):
    name = 'saarland'
    allowed_domains = ['www.uniklinikum-saarland.de']
    start_urls = ['https://www.uniklinikum-saarland.de/de/aktuelles/aktuelles']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="uksnews-list-title"]/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[text()="Nächste >"]'), callback='parse_item', follow=True),
    )

    title_xpath = '//div[@class="uksnews-single-title"]/text()'
    text_xpath = '//div[@class="uksnews-single-content"]/p/descendant::text()'
    # author_xpath = '//div[@id="content"]/p[last()]/em/descendant::text()'
    contentdate_xpath = '//div[@class="uksnews-single-date"]/text()'


    def parse_item(self, response):
        # author_list = response.xpath(self.author_xpath).getall()
        authors = 'UKS'
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
            'labels': 'university'
        }
