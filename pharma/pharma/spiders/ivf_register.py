# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime


class IvfRegisterSpider(scrapy.Spider):
    name = 'ivf-register'
    allowed_domains = ['www.deutsches-ivf-register.de']
    start_urls = ['https://www.deutsches-ivf-register.de/aktuelle-nachrichten-des-dir.php']

    articles_xpath = '//section[@class="content"]/article'
    title_xpath = './/h2/text()'
    text_xpath = './p/descendant::text()'
    # author_xpath = '//span[@class="nobr"]/i/text()'
    # contentdate_xpath = datetime.strptime(date, '%d-%m-%Y')

    def parse(self, response):
        for article in response.xpath(self.articles_xpath):
            text_list = article.xpath(self.text_xpath).getall()
            text = '\n'.join(text_list)
            content_date = datetime.utcnow()
            yield {
                'title': article.xpath(self.title_xpath).get(),
                'author': 'Deutsches IVF-Register e.V. (D·I·R)',
                'content_text': text,
                'content_date': content_date,
                'url': response.url,
                'url_base': self.allowed_domains[0],
                'labels': 'news'
            }
