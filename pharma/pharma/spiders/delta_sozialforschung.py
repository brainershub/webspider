# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from parsel.selector import Selector, SelectorList



class DeltaSozialforschungSpider(scrapy.Spider):
    name = 'delta-sozialforschung'
    allowed_domains = ['www.delta-sozialforschung.de']
    start_urls = ['https://www.delta-sozialforschung.de/news']

    # rules = (
    #     Rule(LinkExtractor(restrict_xpaths='//div[@class="news-element"]/a'), callback='parse_item', follow=True),
    #     # Rule(LinkExtractor(restrict_xpaths='//li[@class="hcf-paging-forward"][1]/a'), callback='parse_item', follow=True),
    # )

    title_xpath = '//div[@class="col-sm-12 col-md-12 col-lg-8"]/child::h2[1]/text()'
    text_xpath = '//div[@class="col-sm-12 col-md-12 col-lg-8"]/child::h2[1]/following-sibling::p/descendant::text()'
    
    def parse(self, response):
        articles = response.xpath('//div[@class="news-element"]')
        for a in articles:
            url=a.xpath('./child::a')
            if isinstance(url, SelectorList) and url is not None:
                yield response.follow(
                    url=url[0], 
                    callback=self.parse_item, 
                    meta={'date': a.xpath('//small/text()').get()})
            elif url is None:
                print('URL IS NONE')
            else:
                yield response.follow(url=url, callback=self.parse_item, meta={'date': a.xpath('//small/text()').get()})

    def parse_item(self, response):
        authors = 'DELTA-Institut für Sozial- und Ökologieforschung GmbH'
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)

        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': authors,
            'content_text': text,
            'content_date': response.meta.get('date'),
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'news'
        }
