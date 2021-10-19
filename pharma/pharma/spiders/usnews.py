# -*- coding: utf-8 -*-
import scrapy


class UsnewsSpider(scrapy.Spider):
    name = 'usnews'
    allowed_domains = ['health.usnews.com']
    start_urls = ['https://health.usnews.com/']

    title_xpath = '//h1/text()'
    text_xpath = '//*[@id="ad-in-text-target"]/descendant::text()'
    author_xpath = '//div[contains(@class, "AuthorWrapper")]/span[text()="By"]/span/a/text()'
    contentdate_xpath = '//div[contains(@class, "AuthorWrapper")]/span[not(child::span)]/text()'


    def parse(self, response):
        links = response.xpath('//h3/a')
        for link in links:
            yield response.follow(url=link, callback=self.parse_page)


    def parse_page(self, response):
        author_list = response.xpath(self.author_xpath).getall()
        if author_list:
            authors = author_list
        else:
            authors = 'None'
        authors = ','.join(author_list)

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
