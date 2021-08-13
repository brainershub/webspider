# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime

from pharma.features import clean_date

class RepromedSpider(scrapy.Spider):
    name = 'repromed'
    allowed_domains = ['repromed.de']
    start_urls = ['https://repromed.de/service/aktuelles']

    articles_xpath = '//*[@id="main"]/article'
    title_xpath = './/h2/text()'
    text_xpath = './/div[@class="entry-content"]/p/descendant::text()'
    # author_xpath = '//span[@class="nobr"]/i/text()'
    # contentdate_xpath = datetime.strptime(date, '%d-%m-%Y')

    def parse(self, response):
        for article in response.xpath(self.articles_xpath):
            text_list = article.xpath(self.text_xpath).getall()
            text = '\n'.join(text_list)
            content_date = datetime.utcnow()
            yield {
                'title': article.xpath(self.title_xpath).get(),
                'author': 'BRZ',
                'content_text': text,
                'content_date': content_date,
                'url': response.url,
                'url_base': self.allowed_domains[0],
                'labels': 'news'
            }