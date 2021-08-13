# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date


class KmaOnlineSpider(CrawlSpider):
    name = 'kma-online'
    allowed_domains = ['www.kma-online.de']
    start_urls = ['https://www.kma-online.de/aktuelles/klinik-news',
    'https://www.kma-online.de/aktuelles/medizintechnik',
    'https://www.kma-online.de/aktuelles/medizin',
    'https://www.kma-online.de/aktuelles/pflege',
    'https://www.kma-online.de/aktuelles/it-digital-health'
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h4/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//li[@class="next"]/a'), callback='parse_item', follow=True),
    )

    title_xpath = '//h2[@itemprop="headline"]/text()'
    text_xpath = '//p[@class="bodytext"]/descendant::text()'
    author_xpath = 'substring-after(//time/following-sibling::text(), "Quelle:")'
    contentdate_xpath = '//time/@datetime'


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
            'labels': 'news'
        }
