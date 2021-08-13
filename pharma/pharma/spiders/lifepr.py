# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date


class LifeprSpider(CrawlSpider):
    name = 'lifepr'
    allowed_domains = ['www.lifepr.de']
    start_urls = ['https://www.lifepr.de/kategorie/gesundheitmedizin']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h1/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[text()="nächste Seite"]'), callback='parse_item', follow=True),
    )

    title_xpath = '//h1[@itemprop="headline"]/text()'
    text_xpath = '//div[@itemprop="articleBody"]/descendant::text()'
    author_xpath = '//div[@class="content-wrapper"]/text()[1]'
    contentdate_xpath = '//span[@itemprop="dateline"]/time/text()'


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
