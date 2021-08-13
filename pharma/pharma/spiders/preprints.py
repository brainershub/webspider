import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class PreprintsSpider(scrapy.Spider):
    name = 'preprints'
    allowed_domains = ['www.preprints.org']
    start_urls = ['https://www.preprints.org/subject/browse/all?page_num=1']

    def parse(self, response):
        articles = response.xpath('//a[@class="title"]/@href').getall()
        dates = response.xpath('//div[@class="show-for-large-up"]/span/text()').getall()
        yield from response.follow_all(articles, self.parse_page, meta={'content_date': articles.xpath('//a[@class="title"]/parent::div/parent::div/following-sibling::div[@class="show-for-large-up"]/span/text()').get()})

    def parse_page(self, response):
        authors_list = response.xpath('div[@class="manuscript-authors"]/span/a/text()').getall()
        authors = ', '.join(authors_list)
        text_list = response.xpath('//div[@id="submission-content"]/div[not(@class)]/descendant::text()').getall()
        text = '\n'.join(text_list)
        yield {
            'title': response.xpath('//h1/text()').get(),
                'author': authors,
                'content_text': text,
                'content_date': response.meta['content_date'],
                'url': response.url,
                'url_base': self.allowed_domains[0],
                'labels': 'journal'
        }

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(PreprintsSpider)
    process.start()