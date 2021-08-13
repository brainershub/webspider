# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date


class SpektrumSpider(CrawlSpider):
    name = 'spektrum'
    allowed_domains = ['www.spektrum.de']
    start_urls = ['https://www.spektrum.de/biologie',
    'https://www.spektrum.de/medizin',
    'https://www.spektrum.de/psychologie-hirnforschung'
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//article/a'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//li[@class="next"]/a'), callback='parse_item', follow=True),
    )

    title_xpath = '//span[@class="content__title"]/text()'
    text_xpath = '//div[@class="row align-center"]/div/p/descendant::text()'
    author_xpath = '//div[@class="content__author"]/span/a/text()'
    contentdate_xpath = '//li[@class="item content__meta__date"]/text()'


    def parse_item(self, response):
        author_list = response.xpath(self.author_xpath).get()
        # if author_list:
        #     authors = author_list
        # else:
        #     authors = 'None'
        authors = author_list
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
