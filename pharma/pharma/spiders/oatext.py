import scrapy


class OatextSpider(scrapy.Spider):
    name = 'oatext'
    allowed_domains = ['www.oatext.com']
    start_url = ['https://www.oatext.com/index.php']

    title_xpath = '//h2/a/text()'
    author_xpath = '//p[contains(@class, "title")]/text()'
    # contentdate_xpath = 'substring-after(//span[@class="text2"]/text()[2], "Accepted")'
    text_xpath = '//div[@class="text-justify"]/descendant::text()'

    def parse(self, response):
        links = response.xpath('//a[text()="Abstract"]')
        for l in links:
            yield response.follow(url=l, callback=self.parse_page)
        

    def parse_page(self, response):
        author_list = response.xpath(self.author_xpath).getall()
        authors = ', '.join(author_list)
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        # content_date_raw = response.xpath(self.contentdate_xpath).get()
        
        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': authors,
            'content_text': text,
            'content_date': response.meta.get('date'),
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }