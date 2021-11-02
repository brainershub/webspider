# -*- coding: utf-8 -*-
import scrapy


class BmjSpider(scrapy.Spider):
    name = 'bmj'
    allowed_domains = ['srh.bmj.com']
    start_urls = ['https://srh.bmj.com']

    title_xpath = '//cite/div/text()'
    text_xpath = '//div[contains(@id, "abstract")]/descendant::text()'
    author_xpath = '//span[@class="name"]/text()'
    # contentdate_xpath = 'substring-after(//strong[1]/text(), ",")'

    def parse(self, response):
        articles = response.xpath('//article[not(@class)]')
        for article in articles:
            url = article.xpath('./h4/a')
            date = article.xpath('./footer/time/text()').get()
            yield response.follow(url=url[0], callback=self.parse_item, meta={'date': date})
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
            'content_date': response.meta.get('date'),
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }
