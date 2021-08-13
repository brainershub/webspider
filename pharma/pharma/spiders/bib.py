# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date


class BibSpider(CrawlSpider):
    name = 'bib'
    allowed_domains = ['www.bib.bund.de']
    start_urls = ['https://www.bib.bund.de/DE/Aktuelles/Aktuelles.html']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="teaser type-1 row"]//h2/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="forward button"]'), callback='parse_item', follow=True),
    )

    title_xpath = '//h1[@class="isFirstInSlot"]/text()'
    text_xpath = '//div[@id="content"]/p/descendant::text()'
    author_xpath = '//div[@id="content"]/p[last()]/em/descendant::text()'
    contentdate_xpath = 'substring-after(//span[@class="dachzeile"], "•")'


    def parse_item(self, response):
        author_list = response.xpath(self.author_xpath).getall()
        authors = ' '.join(author_list)
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
