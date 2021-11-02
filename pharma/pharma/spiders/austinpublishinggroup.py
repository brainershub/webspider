import scrapy

class AustinpublishinggroupSpider(scrapy.Spider):
    name = 'austinpublishinggroup'
    allowed_domains = ['austinpublishinggroup.com']
    start_urls = ['https://austinpublishinggroup.com/reproductive-medicine']

    title_xpath = '//h1/text()'
    author_xpath = '//p[@class="subline"]/text()'
    contentdate_xpath = '//strong[text()="Published: "]/following-sibling::text()'
    text_xpath = '//div[@class="article"]//p/descendant::text()'

    def parse(self, response):
        links = response.xpath('//h3/a')
        for l in links:
            yield response.follow(url=l, callback=self.parse_page)
        

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