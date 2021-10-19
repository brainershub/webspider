from scrapy import Spider

class GbaSpider(Spider):
    name = 'g-ba'
    allowed_domains = ['www.g-ba.de']
    start_urls = ['https://www.g-ba.de/letzte-aenderungen']

    title_xpath = '//h1/text()'
    # author_xpath = '//a[@data-test="author-name"]/text()'
    # contentdate_xpath = '//p[text()="Published"]/descendant::time/text()'
    text_xpath = '//div[@class="gba-content"]/descendant::text()'

    def parse(self, response):
        links = response.xpath('//h2/a')
        for l in links:
            yield response.follow(url=l, callback=self.parse_page, meta={'date': response.xpath('//main/ul/li/div[contains(@class, "datum")]/text()').get()})
        
        # next_page = response.xpath('//div[@id="sort-results"]/following-sibling::form/a[@class="next"]/@href')
        # if next_page is not None:
        #     if next_page is SelectorList:
        #         yield response.follow(url=next_page[0], callback=self.parse)
        #     else:
        #         yield response.follow(url=next_page, callback=self.parse)
        

    def parse_page(self, response):
        # author_list = response.xpath(self.author_xpath).getall()
        # authors = ', '.join(author_list)
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        # content_date_raw = response.xpath(self.contentdate_xpath).get()
        
        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': 'Gemeinsamer Bundesausschuss',
            'content_text': text,
            'content_date': response.meta.get('date'),
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'news'
        }