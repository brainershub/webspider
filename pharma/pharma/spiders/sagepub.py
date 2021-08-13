# -*- coding: utf-8 -*-
import scrapy

from pharma.features import clean_date

class SagepubSpider(scrapy.Spider):
    name = 'sagepub'
    allowed_domains = ['journals.sagepub.com']
    start_urls = [r'https://journals.sagepub.com/action/showPublications?pageSize=20&startPage=0']


    title_xpath = '//h1/text()'
    text_xpath = '//article[@class="article"]//p/descendant::text()'
    author_xpath = '//a[@class="entryAuthor" and child::text() and parent::div[@class="header"]]/text()'
    contentdate_xpath = '//span[@class="publicationContentEpubDate dates"]/text()[last()]'

    def parse(self, response):
        links = response.xpath('//div[@class="results"]/form/table/tbody/tr//a/@href').getall()
        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_page)

    def parse_page(self, response):
        links = response.xpath('//div[@class="title"]/a/@href').getall()
        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_item)

    def parse_item(self, response):
        author_list = response.xpath(self.author_xpath).getall()
        # if author_list:
        #     authors = author_list
        # else:
        #     authors = 'None'
        authors = ', '.join(author_list)
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
            'labels': 'journal'
        }

