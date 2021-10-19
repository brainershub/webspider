import scrapy
from scrapy.selector.unified import SelectorList

class TandfonlineSpider(scrapy.Spider):
    name = 'tandfonline'
    allowed_domains = ['www.tandfonline.com']
    start_urls = [
                    # 'https://www.tandfonline.com',
                    'https://www.tandfonline.com/topic/allsubjects/me?target=topic&ConceptID=4272',
                    'https://www.tandfonline.com/topic/allsubjects/hs?target=topic&ConceptID=4266',
                    'https://www.tandfonline.com/topic/allsubjects/bs?target=topic&ConceptID=4253'
                ]

    title_xpath = '//h1[not(@class)]//text()'
    text_xpath = '//p[@class="summary-title"]/following-sibling::*/descendant::text() | //div[@class="hlFld-Fulltext"]//p/descendant::text() | //*[contains(@class, "hlFld-Abstract")]/descendant::text()'
    author_xpath = '//a[@class="author"]/text()'
    contentdate_xpath = 'substring-after(//div[contains(text(), "Published")]/text(), ":")'

    # def parse(self, response):
    #     links = response.xpath('//h3[not(@class)]/a')
    #     for link in links:
    #         yield response.follow(url=link, callback=self.parse_page)

    def parse(self, response):
        links = response.xpath('//article[@class="searchResultItem"]/div[@class="art_title"]//a')
        next_page = response.xpath('//a[contains(@class, "nextPage")]')
        for link in links:
            yield response.follow(url=link, callback=self.parse_item)
        
        if next_page is not None:
            if isinstance(next_page, SelectorList):
                yield response.follow(url=next_page[0], callback=self.parse)
            else:
                yield response.follow(url=next_page, callback=self.parse)
        

    def parse_item(self, response):
        author_list = response.xpath(self.author_xpath).getall()
        authors = ', '.join(author_list)
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        content_date_raw = response.xpath(self.contentdate_xpath).get()
        # content_date_clean = content_date_raw.split(':')
        
        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': authors,
            'content_text': text,
            'content_date': content_date_raw,
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }
