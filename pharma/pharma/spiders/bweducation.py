# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class BweducationSpider(CrawlSpider):
    name = 'bweducation'
    allowed_domains = ['bweducation.businessworld.in']
    start_urls = ['http://bweducation.businessworld.in/news']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="item-content"]/h3/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="next page-numbers"]'), follow=True),
    )

    title_xpath = '//h1[@class="big_article_header"]/text()'
    text_xpath = '//div[contains(@class,"article_text")]/descendant::text()'
    author_xpath = '//span[@class="author"]/a/text()'
    # contentdate_xpath = '//div[@class="post-meta"]//span[@class="date "]/text()'
    contantdate_x = '//span[@class="date"]/text()'
    contantmonth_x = '//span[@class="month"]/a/text()'


    def parse_item(self, response):
        author_list = response.xpath(self.author_xpath).get()
        # if author_list:
        #     authors = author_list
        # else:
        #     authors = 'None'
        authors = author_list
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        day = response.xpath(self.contantdate_x).get()
        month = response.xpath(self.contantmonth_x).get()
        date = [day, month]
        content_date_raw = ', '.join(date)

        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': authors,
            'content_text': text,
            'content_date': content_date_raw,
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'news'
        }