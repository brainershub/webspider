from parsel.selector import Selector, SelectorList
import scrapy

class AssistedSpider(scrapy.Spider):
    name = 'assisted'
    allowed_domains = ['link.springer.com']
    start_urls = ['https://link.springer.com/search?query=&search-within=Journal&facet-journal-id=10815']

    title_xpath = '//h1/text()'
    author_xpath = '//a[@data-test="author-name"]/text()'
    contentdate_xpath = '//p[text()="Published"]/descendant::time/text()'
    text_xpath = '//div[@class="c-article-section__content"]/descendant::text()'

    def parse(self, response):
        links = response.xpath('//a[@class="title"]')
        for l in links:
            yield response.follow(url=l, callback=self.parse_page)
        
        next_page = response.xpath('//div[@id="sort-results"]/following-sibling::form/a[@class="next"]')
        if next_page is not None:
            if isinstance(next_page, SelectorList):
                yield response.follow(url=next_page[0], callback=self.parse)
            else:
                yield response.follow(url=next_page, callback=self.parse)
        

    def parse_page(self, response):
        title_list = response.xpath(self.title_xpath).getall()
        title = ' '.join(title_list)
        author_list = response.xpath(self.author_xpath).getall()
        authors = ', '.join(author_list)
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        content_date_raw = response.xpath(self.contentdate_xpath).get()
        
        yield {
            'title': title,
            'author': authors,
            'content_text': text,
            'content_date': content_date_raw,
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }