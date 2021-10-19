import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class BioscientificaSpider(scrapy.Spider):
    name = 'bioscientifica'
    allowed_domains = ['rep.bioscientifica.com']
    start_urls = ['https://rep.bioscientifica.com/browse']

    # rules = (
    #     Rule(LinkExtractor(restrict_xpaths='//div[@title="Free access"]/following-sibling::div//a'), callback='parse_item', follow=True),
    #     # Rule(LinkExtractor(restrict_xpaths='//a[@title="Next page"]'), follow=True),
    # )

    title_xpath = '//h1/text()'
    text_xpath = '//div[@class="section"]/descendant::text()'
    author_xpath = '//span[text()="Authors:"]/following-sibling::span/a/text()'
    contentdate_xpath = '//dl[@class="onlinepubdate c-List__items"]/dd/text()'

    def start_requests(self):
        pages = 10
        for i in range(1,pages):
            url = 'https://rep.bioscientifica.com/browse?access=all&page=' + str(i)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.xpath('//div[@title="Free access"]/following-sibling::div//a')
        for link in links:
            yield response.follow(url=link, callback=self.parse_item)


    def parse_item(self, response):
        title_list = response.xpath(self.title_xpath).getall()
        title = ' '.join(title_list)

        author_list = response.xpath(self.author_xpath).getall()
        authors = ', '.join(author_list)

        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)

        content_date_raw = response.xpath(self.contentdate_xpath).get()
        content_date_clean = clean_date(content_date_raw)

        yield {
            'title': title,
            'author': authors,
            'content_text': text,
            'content_date': content_date_clean,
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }

