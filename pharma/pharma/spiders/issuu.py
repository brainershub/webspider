import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class IssuuSpider(CrawlSpider):
    name = 'issuu'
    allowed_domains = ['issuu.com']
    start_urls = ['https://issuu.com/blog']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="sc-dlnjwi oz8a7l-4 fuymzY hYCRKx"]/a'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//ul[@class="pagination pull-right"]/li[1]/a'), follow=True),
    )

    title_xpath = '//h1[@class="ixu-heading ixu-heading--huge"]/text()'
    text_xpath = '//div[@class="sc-dlnjwi sc-14l79ci-1 asrmw hJyIx"]/descendant::text()'
    author_xpath = '//h1[@class="ixu-heading ixu-heading--huge"]/following-sibling::section/span[1]/a/text()'
    contentdate_xpath = '//h1[@class="ixu-heading ixu-heading--huge"]/following-sibling::section/span[3]/a/text()'


    def parse_item(self, response):
        author_list = response.xpath(self.author_xpath).get()
        # if author_list:
        #     authors = author_list
        # else:
        #     authors = 'None'
        authors = author_list
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
            'labels': 'blog'
        }

