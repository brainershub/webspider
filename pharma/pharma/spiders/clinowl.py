# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scrapy.utils.trackref import NoneType

class ClinowlSpider(CrawlSpider):
    name = 'clinowl'
    allowed_domains = ['clinowl.com']
    start_urls = ['https://clinowl.com']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//section[@id="content"]//li/a'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//a[@rel="next"]'), callback='parse_item', follow=True),
    )

    title_xpath = '//h1/text()'
    text_xpath = '//div[@class="entry clearfix"]/p/descendant::text()'
    author_xpath = '//strong[text()="Authors: "]/following-sibling::text()'
    contentdate_xpath = '//time/text()'


    def parse_item(self, response):
        author_list = response.xpath(self.author_xpath).get()
        authors = author_list
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        content_date_raw = response.xpath(self.contentdate_xpath).get()

        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': authors,
            'content_text': text,
            'content_date': content_date_raw,
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(ClinowlSpider)
    process.start()