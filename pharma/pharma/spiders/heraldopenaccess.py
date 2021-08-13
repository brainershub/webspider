import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class HeraldopenaccessSpider(CrawlSpider):
    name = 'heraldopenaccess'
    allowed_domains = ['www.heraldopenaccess.us']
    start_urls = ['https://www.heraldopenaccess.us/journals']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[text()=" Visit Journal"]'), callback='parse_page', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//a[@title="Next page"]'), follow=True),
    )

    title_xpath = '//h3/text()'
    text_xpath = '//div[@class="card-text text-justify mb-4"]/p[not(child::img)]/descendant::text()'
    author_xpath = '//dl[@class="authors"]/dt/em/text()'
    contentdate_xpath = '//strong[text()="Published Date"]/following-sibling::text()'

    def parse_page(self, response):
        links = response.xpath('//h5/a/@href').getall()
        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_item())

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
