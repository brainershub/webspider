# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class RndSpider(CrawlSpider):
    name = 'rnd'
    allowed_domains = ['rnd.de']
    start_urls = ['https://www.rnd.de/gesundheit']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[@class="tsr__lnk"]'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//li[@class="hcf-paging-forward"][1]/a'), callback='parse_item', follow=True),
    )

    title_xpath = '//h2/span[@class="a-hd__h-txt"]/text()'
    text_xpath = '//div[@class="js-a-con a-con"]/descendant::text()[not(ancestor::form)]'
    author_xpath = '//div[@id="a-hd__aut--txt-0"]/text()'
    contentdate_xpath = 'substring-before(//div[@class="a-hd__mta-tm"]/time/text(), ",")'


    def parse_item(self, response):
        author_list = response.xpath(self.author_xpath).get()
        if author_list:
            authors = author_list
        else:
            authors = 'None'
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
