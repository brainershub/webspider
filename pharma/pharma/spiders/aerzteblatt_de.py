# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date


class AerzteblattDeSpider(CrawlSpider):
    name = 'aerzteblatt.de'
    allowed_domains = ['www.aerzteblatt.de']
    start_urls = ['https://www.aerzteblatt.de/nachrichten/medizin', 'https://www.aerzteblatt.de/nachrichten/aerzteschaft']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="newsListItem"]/h2/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[@title="weiter..."]'), follow=True),
    )

    title_xpath = '//h1/text()'
    text_xpath = '//div[@class="newstext"]/p/descendant::text()'
    author_xpath = '//span[@class="nobr"]/i/text()'
    contentdate_xpath = 'substring-after(//h4[1], ",")'


    def parse_item(self, response):
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        content_date_raw = response.xpath(self.contentdate_xpath).get()
        content_date_clean = clean_date(content_date_raw)

        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': response.xpath(self.author_xpath).get(),
            'content_text': text,
            'content_date': content_date_clean,
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'news'
        }