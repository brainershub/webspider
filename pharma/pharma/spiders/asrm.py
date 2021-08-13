import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class AsrmSpider(CrawlSpider):
    name = 'asrm'
    allowed_domains = ['www.asrm.org']
    start_urls = ['https://www.asrm.org/news-and-publications/news-and-research']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//article[@class="article"]/h3/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="pagination pull-right"]/li[1]/a'), follow=True),
    )

    title_xpath = '//article[@class="article"]/h1/text()'
    text_xpath = '//article[@class="article"]/descendant::text()'
    author_xpath = 'substring-after(//article[@class="article"]/p[@class="article__info"]/text()[2], "By:")'
    contentdate_xpath = '//article[@class="article"]/p[@class="article__info"]/text()[1]'


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
            'labels': 'news'
        }

