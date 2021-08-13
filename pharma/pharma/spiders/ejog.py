import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class EjogSpider(CrawlSpider):
    name = 'ejog'
    allowed_domains = ['www.ejog.org']
    start_urls = ['https://www.ejog.org/inpress']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[text()="Full-Text HTML"]'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//ul[@class="pagination pull-right"]/li[1]/a'), follow=True),
    )

    title_xpath = '//h1[@class="article-header__title smaller"]/text()'
    text_xpath = '//div[@class="section-paragraph"]/div[@class="section-paragraph"]/descendant::text()'
    author_xpath = '//li[@class="loa__item author"]/div/a/text()'
    contentdate_xpath = '//span[@class="article-header__publish-date__value"]/text()'


    def parse_item(self, response):
        author_list = response.xpath(self.author_xpath).getall()
        # if author_list:
        #     authors = author_list
        # else:
        #     authors = 'None'
        authors = ', '.join(author_list)
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
            'labels': 'journal'
        }

