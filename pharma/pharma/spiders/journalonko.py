# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date


class JournalonkoSpider(CrawlSpider):
    name = 'journalonko'
    allowed_domains = ['www.journalonko.de']
    start_urls = ['https://www.journalonko.de/news/liste']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[@title="Zum Beitrag"]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[@rel="next"]'), callback='parse_item', follow=True),
    )

    title_xpath = '//h1/text()'
    text_xpath = '//section[@class="vorspann"]/text() | //div[@class="textBox"]/descendant::text()[parent::div or parent::h2]'
    # author_xpath = '//span[@class="contributor"]/text()'
    contentdate_xpath = '//span[@class="newsDate "]/text()'


    def parse_item(self, response):
        # author_list = response.xpath(self.author_xpath).getall()
        authors = 'DKFZ'
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
