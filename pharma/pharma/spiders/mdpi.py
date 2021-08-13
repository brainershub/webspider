# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date


class MdpiSpider(CrawlSpider):
    name = 'mdpi'
    allowed_domains = ['www.mdpi.com']
    start_urls = ['https://www.mdpi.com/search?sort=pubdate&page_count=50']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[@class="title-link"]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//span[@class="pageSelect"]/a[position()=last()-1]'), callback='parse_item', follow=True),
    )

    title_xpath = '//h1/text()'
    text_xpath = '//div[@class="c-article-body u-clearfix"]/p/descendant::text()'
    author_xpath = '//div[@class="art-authors hypothesis_container"]/span/div/a/span/text()'
    contentdate_xpath = '//div[@class="pubhistory"]/text()'


    def parse_item(self, response):
        author_list = response.xpath(self.author_xpath).getall()
        # if author_list:
        #     authors = author_list
        # else:
        #     authors = 'None'
        authors = ' '.join(author_list)
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        content_date_raw = response.xpath(self.contentdate_xpath).get()
        if content_date_raw:
            content_date_first = content_date_raw.split('/')
            content_date_second = content_date_first[0].split(':')
            content_date_clean = clean_date(content_date_second[1])
        else:
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

