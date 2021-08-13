import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class JbcSpider(CrawlSpider):
    name = 'jbc'
    allowed_domains = ['jbc.org']
    start_urls = ['http://www.jbc.org/inpress/']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'

    title_xpath = '//h1[@class="article-header__title"]/text()'
    text_xpath = '//div[@class="section-paragraph"]/child::text()'
    author_xpath = '//div[@class="article-header__middle"]/ul/li//a/text()'
    contentdate_xpath = 'substring-after(//div[@class="article-info__date"]/text()[1], "Accepted: ")'

    def start_requests(self):
        yield scrapy.Request(url='http://www.jbc.org/inpress', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h3[@class="toc__item__title"]/a'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        author_list = response.xpath(self.author_xpath).getall()
        authors = '\n'.join(author_list)
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
            'url_base': self.allowed_domains[0]
        }
