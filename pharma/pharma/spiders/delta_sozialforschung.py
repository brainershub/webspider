# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date


class DeltaSozialforschungSpider(CrawlSpider):
    name = 'delta-sozialforschung'
    allowed_domains = ['www.delta-sozialforschung.de']
    start_urls = ['https://www.delta-sozialforschung.de/news']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="news-element"]/a'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//li[@class="hcf-paging-forward"][1]/a'), callback='parse_item', follow=True),
    )

    title_xpath = '//h1/following-sibling::h2[1]/text()'
    text_xpath = '//h1/following-sibling::p/descendant::text()'
    # author_xpath = '//a[@class="story-customer"]/text()'
    # contentdate_xpath = 'substring-before(//p[@class="date"]/text(), "–")'


    def parse_item(self, response):
        # author_list = response.xpath(self.author_xpath).getall()
        authors = response.xpath(self.author_xpath).get()
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
            'labels': 'news'
        }
