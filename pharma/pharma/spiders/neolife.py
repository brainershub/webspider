# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date


class NeolifeSpider(CrawlSpider):
    name = 'neolife'
    allowed_domains = ['neo.life']
    start_urls = ['https://neo.life/features/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="tease"]/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[@title="Next page"]'), callback='parse_item', follow=True),
    )

    title_xpath = '//h1/text()'
    text_xpath = '//div[@class="basic-text js-hang-punc"]/p/descendant::text() | //div[@class="basic-text js-hang-punc"]/h3/descendant::text()'
    author_xpath = '//a[@class="article__byline-item__author"]/text()'
    contentdate_xpath = 'substring-after(//span[@class="article-footer__author-date"]/text(), "on ")'


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
            'labels': 'blog'
        }
