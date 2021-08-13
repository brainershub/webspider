import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class AcademicSpider(CrawlSpider):
    name = 'academic'
    allowed_domains = ['academic.oup.com']
    start_urls = ['https://academic.oup.com/biolreprod/issue-archive']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//section[@class="master-main row"]/div/div/div/div/a'), callback='parse_page', follow=False),
        # Rule(LinkExtractor(restrict_xpaths='//a[@title="Next page"]'), follow=True),
    )

    title_xpath = '//h1/text()'
    text_xpath = '//div[@class="widget-items"]/descendant::text()'
    author_xpath = '//a[@class="linked-name js-linked-name-trigger"]/text()'
    contentdate_xpath = '//div[@class="citation-date"]/text()'

    def parse_page(self, response):
        links = response.xpath('//div[@class="customLink"]/a/@href').getall()
        
        for link in links:
            # yield scrapy.Request(url=response.urljoin(link), callback=self.parse_item)
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_second_page)

    def parse_second_page(self, response):
        links = response.xpath('//h5[@class="customLink item-title"]/a/@href').getall()
        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_item)


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
