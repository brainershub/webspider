# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class AwmfSpider(CrawlSpider):
    name = 'awmf'
    allowed_domains = ['www.awmf.org']
    start_urls = ['https://www.awmf.org/service-navigation/awmf-aktuell.html']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="news-content"]/a'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//a[@class="js_nextLink"]'), callback='parse_item', follow=True),
    )

    title_xpath = '//h2/text()'
    text_xpath = '//div[@class="news-detail"]/p/descendant::text()'
    # author_xpath = '//a[contains(@class,"loa__item__name") and @title]/text()'
    contentdate_xpath = '//em[@class="date"]/text()'


    def parse_item(self, response):
        # author_list = response.xpath(self.author_xpath).getall()
        # authors = '\n'.join(author_list)
        authors = 'AWMF'
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
