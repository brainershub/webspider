import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class PreprintsSpider(scrapy.Spider):
    name = 'preprints'
    allowed_domains = ['www.preprints.org']
    start_urls = ['https://www.preprints.org/subject/browse/all?page_num=1']

    def parse(self, response):
        articles = response.xpath('//a[@class="title"]')
        for article in articles:
            yield response.follow(url=article, callback=self.parse_page, meta={
                'content_date': response.xpath('//span[contains(text(), "Online")]/text()').get()
                })

    def parse_page(self, response):
        authors_list = response.xpath('div[@class="manuscript-authors"]/span/a/text()').getall()
        authors = ', '.join(authors_list)
        text_list = response.xpath('//div[@id="submission-content"]/div[not(@class)]/descendant::text()').getall()
        text = '\n'.join(text_list)

        c_date_raw = response.meta.get('content_date')
        c_date_split_1 = c_date_raw.split(':')
        c_date_split_2 = c_date_split_1[1].split('(')
        c_date = c_date_split_2[0]

        yield {
            'title': response.xpath('//h1/text()').get(),
                'author': authors,
                'content_text': text,
                'content_date': c_date,
                'url': response.url,
                'url_base': self.allowed_domains[0],
                'labels': 'journal'
        }

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(PreprintsSpider)
    process.start()