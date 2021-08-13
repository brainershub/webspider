# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date


class RbmojournalSpider(CrawlSpider):
    name = 'rbmojournal'
    allowed_domains = ['www.rbmojournal.com']
    start_urls = ['https://www.rbmojournal.com/inpress']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h3[@class="toc__item__title"]/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="js_nextLink"]'), callback='parse_item', follow=True),
    )

    title_xpath = '//h1[@class="article-header__title smaller"]/text()'
    text_xpath = '//div[@class="section-paragraph"]/child::text()'
    author_xpath = '//a[contains(@class,"loa__item__name") and @title]/text()'
    contentdate_xpath = '//span[contains(@class,"date__value")]/text()'


    def parse_item(self, response):
        author_list = response.xpath(self.author_xpath).getall()
        authors = '\n'.join(author_list)
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