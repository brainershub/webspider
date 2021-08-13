# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class StatnewsSpider(CrawlSpider):
    name = 'statnews'
    allowed_domains = ['www.statnews.com']
    start_urls = ['https://www.statnews.com/category/pharma',
    'https://www.statnews.com/category/biotech',
    'https://www.statnews.com/category/politics',
    'https://www.statnews.com/category/health-tech',
    'https://www.statnews.com/category/business',
    'https://www.statnews.com/category/health'
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//article/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="next"]/p/a'), callback='parse_item', follow=True),
    )

    title_xpath = '//h1/text()'
    text_xpath = '//section[@class="the-content"]/p/descendant::text()'
    author_xpath = '//div[@class="post-meta"]/p/a[not(@target)]/text()'
    contentdate_xpath = '//div[@class="post-meta"]//span[@class="date "]/text()'


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