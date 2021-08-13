# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class LeopoldinaSpider(CrawlSpider):
    name = 'leopoldina'
    allowed_domains = ['www.leopoldina.org']
    start_urls = ['https://www.leopoldina.org/presse/pressemitteilungen']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h2[@class="presstitle"]/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//li[@class="next"]/a'), callback='parse_item', follow=True),
    )

    title_xpath = '//div[@class="content clearfix"]//h1/text()'
    text_xpath = '//p[@class="bodytext"]/descendant::text()'
    author_xpath = '//div[@class="kontakt-part"]/h2/text()'
    contentdate_xpath = 'substring-after(//span[@class="leo-inline-datetime"]/text(), ",")'
    # contentdate_xpath = '//span[@class="leo-inline-datetime"]/text()'


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
            'labels': 'news'
        }
