# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class KinderwunschSpider(CrawlSpider):
    name = 'kinderwunsch'
    allowed_domains = ['www.kinderwunsch-blog.com']
    start_urls = ['https://www.kinderwunsch-blog.com/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h2[@class="posts_title"]/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[text()="Next ›"]'), callback='parse_item', follow=True),
    )

    title_xpath = '//h2[@class="posts_title"]/text()'
    text_xpath = '//div[@class="entry"]/p[child::text()]/descendant::text()'
    author_xpath = '//a[@rel="author"]/text()'
    contentdate_xpath = '//div[@class="meta"]/a[2]/text()'


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
