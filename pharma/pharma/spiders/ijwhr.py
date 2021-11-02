# -*- coding: utf-8 -*-
import scrapy


class IjwhrSpider(scrapy.Spider):
    name = 'ijwhr'
    allowed_domains = ['www.ijwhr.net']
    start_urls = ['https://www.ijwhr.net']

    title_xpath = '//table//tr[2]//b/text()'
    text_xpath = '//div[@align="justify"]/descendant::text()'
    author_xpath = '//font[@class="normal"]/a/text()'
    contentdate_xpath = 'substring-before(//span[@class="turuncu_but_222"]/span/text(), ",")'

    def parse(self, response):
        articles = response.xpath('//a[@class="article_title"]')
        for article in articles:
            yield response.follow(url=article, callback=self.parse_item)
        # next_page = response.xpath('//ol[@class="pagination"]/li[2]//a')
        # if next_page is not None:
        #     try:
        #         yield response.follow(url=next_page, callback=self.parse)
        #     except:
        #         yield response.follow(url=next_page[0], callback=self.parse)

    def parse_item(self, response):
        author_list = response.xpath(self.author_xpath).getall()
        authors = '\n'.join(author_list)
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)

        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': authors,
            'content_text': text,
            'content_date': response.xpath(self.contentdate_xpath).get(),
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }
