import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class ScienceblogSpider(CrawlSpider):
    name = 'scienceblog'
    allowed_domains = ['scienceblogs.de']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'

    title_xpath = '//h1//text()'
    text_xpath = '//div[@class="main"]/div/descendant::p//text()'
    author_xpath = '//a[@rel="author"]/text()'
    contentdate_xpath = '//div[@class="content entry-meta"]/span/following-sibling::text()[1]'

    def start_requests(self):
        yield scrapy.Request(url='https://scienceblogs.de/channel/medizin', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h2[@class="entry-title"]/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="next"]'), callback='parse_item', follow=True),
    )

    # def set_user_agent(self, request):
    #     request.headers['User-Agent'] = self.user_agent
    #     return request

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
            'labels': 'blog'
        }
