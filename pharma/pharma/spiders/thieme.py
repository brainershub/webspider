import scrapy
from scrapy.selector import SelectorList

class thiemeSpider(scrapy.Spider):
    name = 'thieme'
    allowed_domains = ['www.thieme.de']
    start_urls = ['https://www.thieme.de/de/presse/pressemitteilungen-203.htm']

    title_xpath = '//h1/text()'
    # author_xpath = '//h1[@class="entry-title"]/following-sibling::span[@class="author-links"]/span[last()]/a/text()'
    # contentdate_xpath = '//div[@class="article-date"]/text()'
    text_xpath = '//h1/following-sibling::*/descendant::text()'

    def parse(self, response):
        links = response.xpath('//ul[@class="content pages"]/li//a')
        for l in links:
            # url = l.xpath('.//a/@href')
            date = l.xpath('./preceding-sibling::span[@class="date"]/text()').get()
            yield response.follow(url=l, 
            callback=self.parse_page,
            meta={'date': date})
        
        next_page = response.xpath('//a[@class="next"]')
        if next_page is not None:
            if isinstance(next_page, SelectorList):
                yield response.follow(url=next_page[0], callback=self.parse)
            else:
                yield response.follow(url=next_page, callback=self.parse)
        

    def parse_page(self, response):
        # author_list = response.xpath(self.author_xpath).getall()
        # authors = ', '.join(author_list)
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        # content_date_raw = response.xpath(self.contentdate_xpath).get()
        
        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': 'Thieme',
            'content_text': text,
            'content_date': response.meta.get('date'),
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'blog'
        }