# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date


class IdwOnlineSpider(CrawlSpider):
    name = 'idw-online'
    allowed_domains = ['idw-online.de']
    start_urls = ['https://idw-online.de/de/?sort=time']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h6/a'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//li[@class="hcf-paging-forward"][1]/a'), callback='parse_item', follow=True),
    )

    title_xpath = '//h4[following-sibling::h5]text()'
    text_xpath = '//h5/following-sibling::p/descendant::text()'
    author_xpath = '//h5[@class="subheader" and preceding-sibling::h4]/text()'
    contentdate_xpath = '//div[@class="blueline-top add-padding-h"]/em/text()'


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
            'labels': 'news'
        }
