import scrapy
from scrapy.selector.unified import SelectorList

class CambridgeSpider(scrapy.Spider):
    name = 'cambridge'
    allowed_domains = ['www.cambridge.org']
    start_urls = ['https://www.cambridge.org/de/academic/news']

    title_xpath = '//h1/text()'
    # author_xpath = '//h1[@class="entry-title"]/following-sibling::span[@class="author-links"]/span[last()]/a/text()'
    contentdate_xpath = '//div[@class="article-date"]/text()'
    text_xpath = '//div[@class="article-date"]/following-sibling::*/descendant::text()'

    def parse(self, response):
        links = response.xpath('//ul[@class="newsListing"]/li/a')
        for l in links:
            yield response.follow(url=l, callback=self.parse_page)
        
        next_page = response.xpath('//li[@class="next"]//a')
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
            'author': 'Cambridge Academic',
            'content_text': text,
            'content_date': response.meta.get('date'),
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'news'
        }