import scrapy


class SundayvisionSpider(scrapy.Spider):
    name = 'sundayvision'
    allowed_domains = ['www.sundayvision.co.ug']
    start_url = ['https://www.sundayvision.co.ug/science']

    title_xpath = '//h1/text()'
    author_xpath = '//h1[@class="entry-title"]/following-sibling::span[@class="author-links"]/span[last()]/a/text()'
    # contentdate_xpath = 'substring-after(//span[@class="text2"]/text()[2], "Accepted")'
    text_xpath = '//div[@class="entry-content"]//p/descendant::text()'

    def parse(self, response):
        links = response.xpath('//h3/a')
        for l in links:
            yield response.follow(url=l, callback=self.parse_page)
        
        next_page = response.xpath('//a[@class="next page-numbers"]')
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse)
        

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