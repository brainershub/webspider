# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class NatureSpider(CrawlSpider):
    name = 'nature'
    allowed_domains = ['nature.com']
    start_urls = ['https://www.nature.com/latest-news',
    'https://www.nature.com/research-analysis'
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[contains(@data-track-label, "article card")]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//li[@data-page="next"]/a'), callback='parse_item', follow=True),
    )

    title_xpath = '//h1/text()'
    text_xpath = '//div[@class="c-article-body u-clearfix"]/p/descendant::text()'
    author_xpath = '//a[@data-test="author-name"]/text()'
    contentdate_xpath = '//time[@itemprop="datePublished"]/text()'


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
