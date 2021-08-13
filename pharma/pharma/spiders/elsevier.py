# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date


class ElsevierSpider(CrawlSpider):
    name = 'elsevier'
    allowed_domains = ['www.elsevier.com']
    start_urls = ['https://www.elsevier.com/about/press-releases']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[@class="press-release-heading"]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//li[contains(@class, "next-link")]/a'), callback='parse_item', follow=True),
    )

    title_xpath = '//h1/text()'
    text_xpath = '//*[@id="maincontent"]//p[child::text()]/descendant::text()'
    # author_xpath = '//a[contains(@class,"loa__item__name") and @title]/text()'
    contentdate_xpath = 'substring-after(//strong[1]/text(), ",")'


    def parse_item(self, response):
        # author_list = response.xpath(self.author_xpath).getall()
        # authors = '\n'.join(author_list)
        authors = 'elsevier'
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
