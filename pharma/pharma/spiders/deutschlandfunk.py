import scrapy

class DeutschlandfunkSpider(scrapy.Spider):
    name = 'deutschlandfunk'
    allowed_domains = ['www.deutschlandfunk.de']
    start_urls = ['https://www.deutschlandfunk.de/die-nachrichten.1441.de.html']

    title_xpath = '//h1/text()[last()]'
    # author_xpath = '//a[@data-test="author-name"]/text()'
    contentdate_xpath = '//div[@class="articlehead"]/header/time/text()'
    text_xpath = '//div[@class="articlemain"]/descendant::text()'

    def parse(self, response):
        links = response.xpath('//h3/a')
        for l in links:
            yield response.follow(url=l, callback=self.parse_page)
        
        # next_page = response.xpath('//div[@id="sort-results"]/following-sibling::form/a[@class="next"]/@href')
        # if next_page is not None:
        #     if isinstance(next_page, SelectorList):
        #         yield response.follow(url=next_page[0], callback=self.parse)
        #     else:
        #         yield response.follow(url=next_page, callback=self.parse)
        

    def parse_page(self, response):
        title_list = response.xpath(self.title_xpath).getall()
        title = ' '.join(title_list)
        # author_list = response.xpath(self.author_xpath).getall()
        # authors = ', '.join(author_list)
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        content_date_raw = response.xpath(self.contentdate_xpath).get()
        
        yield {
            'title': title,
            'author': 'Deutschlandfunk',
            'content_text': text,
            'content_date': content_date_raw,
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'news'
        }