import scrapy

class GuttmacherSpider(scrapy.Spider):
    name = 'guttmacher'
    allowed_domains = ['www.guttmacher.org']
    start_urls = ['https://www.guttmacher.org/journals/ipsrh']

    title_xpath = '//h1[@class="article-title"]/text()'
    author_xpath = '//span[@class="author-name"]/text()'
    contentdate_xpath = '//span[@class="article-published"]/span/text()'
    text_xpath = '//section[@class="abstract"]/descendant::text()'

    

    def parse(self, response):
        links = response.xpath('//h3/a')
        for link in links:
            yield response.follow(url=link, callback=self.parse_page)
        
        next_page = response.xpath('//a[@title="Go to next page"]')
        
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse)

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
