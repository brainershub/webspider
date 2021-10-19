import scrapy

class MedsciSpider(scrapy.Spider):
    name = 'medsci'
    allowed_domains = ['www.medsci.org']
    start_urls = ['https://www.medsci.org/ms/archive']

    title_xpath = '//h1[@class="title"]/text()'
    author_xpath = '//p[@class="author"]/text()'
    contentdate_xpath = 'substring-after(//span[@class="text2"]/text()[2], "Accepted")'
    text_xpath = '//div[@class="content"]/p[not(@class)]/descendant::text() | //div[@class="content"]/p[not(@class)]/preceding-sibling::h2/text()'

    def parse(self, response):
        links = response.xpath('//table[@class="tdshade"][1]//a')
        for l in links:
            yield response.follow(url=l, callback=self.parse_volumes)
        
    def parse_volumes(self, response):
        articles = response.xpath('//a[text()="Full text"]')
        for a in articles:
            yield response.follow(url=a, callback=self.parse_page)

    def parse_page(self, response):
        author_list = response.xpath(self.author_xpath).getall()
        authors = ', '.join(author_list)
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        content_date_raw = response.xpath(self.contentdate_xpath).get()
        
        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': authors,
            'content_text': text,
            'content_date': content_date_raw,
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }