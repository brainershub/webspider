# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class ResearchgateSpider(CrawlSpider):
    name = 'researchgate'
    allowed_domains = ['www.researchgate.net']
    start_urls = ['https://www.researchgate.net/blog']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h1/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[contains(@class, " navi-next")]'), follow=True),
    )

    title_xpath = '//h1[@class="post-title"]/text()'
    text_xpath = '//div[@class="post-body"]/descendant::text()'
    author_xpath = '//div[@class="post-body"]/div/a[1]/text()'
    contentdate_xpath = '//div[@class="post-date"]/text()'

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
            'labels': 'blog'
        }

