# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date


class TagesspiegelSpider(CrawlSpider):
    name = 'tagesspiegel'
    allowed_domains = ['www.tagesspiegel.de']
    start_urls = ['https://www.tagesspiegel.de/suchergebnis/?p=suche&sw=medizin']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//li[contains(@class, "hcf-teaser ")]/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//li[@class="hcf-paging-forward"][1]/a'), callback='parse_item', follow=True),
    )

    title_xpath = '//h1[@class="ts-title"]/span[@class="ts-headline"]/text()'
    text_xpath = '//div[@class="ts-article-content"]/div/p[child::text()]/descendant::text()'
    # author_xpath = '//span[@class="contributor"]/text()'
    contentdate_xpath = 'substring-before(//time[@itemprop="datePublished"]/text(), ",")'


    def parse_item(self, response):
        # author_list = response.xpath(self.author_xpath).getall()
        authors = 'Tagesspiegel'
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
