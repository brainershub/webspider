# -*- coding: utf-8 -*-
from datetime import datetime
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date


class KupSpider(CrawlSpider):
    name = 'kup'
    allowed_domains = ['www.kup.at']
    start_urls = ['https://www.kup.at/journals/reproduktionsmedizin']
    content_date = ''

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//table[@class="inhaltsverzeichnis" and position()=last()]/tbody/tr[child::td]//a[text()="Volltext (HTML)"]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[text()="Ältere Ausgabe"]'), callback='parse_item', follow=True),
    )

    title_xpath = '//h1[@class="Artikel_Art-Titel"]/text()'
    text_xpath = '//p[@class="PR-Flie--"]/descendant::text()'
    author_xpath = '//table[@class="inhaltsverzeichnis"]//th[@class="content"]/text()'
    # contentdate_xpath = '//time/@datetime'

    def parse_item(self, response):
        authors = response.xpath(self.author_xpath).get()
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        # content_date_raw = response.xpath(self.contentdate_xpath).get()
        # content_date_clean = clean_date(content_date_raw)
        # content_date_clean = datetime.strptime(response.xpath(self.contentdate_xpath).get().strftime("%d-%m-%Y"), '%d-%m-%Y')

        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': authors,
            'content_text': text,
            'content_date': datetime.utcnow(),
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }