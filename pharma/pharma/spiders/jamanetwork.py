# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class JamanetworkSpider(CrawlSpider):
    name = 'jamanetwork'
    allowed_domains = ['jamanetwork.com']
    start_urls = ['https://jamanetwork.com/journals/jama/currentissue',
    'https://jamanetwork.com/journals/jamanetworkopen/currentissue',
    'https://jamanetwork.com/journals/jamacardiology/newonline',
    'https://jamanetwork.com/journals/jamadermatology/newonline',
    'https://jamanetwork.com/journals/jama-health-forum/currentissue',
    'https://jamanetwork.com/journals/jamainternalmedicine/newonline',
    'https://jamanetwork.com/journals/jamaneurology/newonline',
    'https://jamanetwork.com/journals/jamaoncology/newonline',
    'https://jamanetwork.com/journals/jamaophthalmology/newonline'
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h3[@class="article--title"]/a'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//a[@rel="next"]'), callback='parse_item', follow=True),
    )

    title_xpath = '//h1/text()'
    text_xpath = '//div[@class="article-full-text"]/descendant::text()'
    author_xpath = '//span[@class="wi-fullname brand-fg"]/a/text()'
    # contentdate_xpath = '//article//li/a/time/text()'
    day_x = '//span[@class="day"]/text()'
    month_x = '//span[@class="month"]/text()'
    year_x = '//span[@class="year"]/text()'


    def parse_item(self, response):
        author_list = response.xpath(self.author_xpath).getall()
        # if author_list:
        #     authors = author_list
        # else:
        #     authors = 'None'
        authors = ', '.join(author_list)
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        day = response.xpath(self.day_x).get()
        month = response.xpath(self.month_x).get()
        year = response.xpath(self.year_x).get()
        date_list = [day, month, year]
        content_date_raw = ' '.join(date_list)
        if content_date_raw:
            content_date_clean = clean_date(content_date_raw)
        else:
            content_date_clean = content_date_raw

        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': authors,
            'content_text': text,
            'content_date': content_date_clean,
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }

