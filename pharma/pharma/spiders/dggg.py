# -*- coding: utf-8 -*-
import scrapy


class DgggSpider(scrapy.Spider):
    name = 'dggg'
    allowed_domains = ['www.dggg.de']
    start_urls = ['https://www.dggg.de/presse/pressemitteilungen-und-nachrichten']

    title_xpath = '//h1/text()'
    text_xpath = '//div[@class="rte"]/p/descendant::text()'
    author_xpath = '//h2[text()="Pressestelle"]/following-sibling::p/strong/text()'
    # contentdate_xpath = '//time[@itemprop="datePublished"]/text()'


    def parse(self, response):
        next_page = response.xpath('//a[@title="Nächste Seite"]/@href').get()
        links = response.xpath('//h2[@class="news-title"]/a')
        for link in links:
            yield response.follow(url=link, callback=self.parse_page, meta={'date': link.xpath('//h2[@class="news-title"]/preceding-sibling::div/span/text()').get()})
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse)


    def parse_page(self, response):
        author_list = response.xpath(self.author_xpath).get()
        # if author_list:
        #     authors = author_list
        # else:
        #     authors = 'None'
        authors = author_list
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
