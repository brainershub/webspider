import scrapy

class JastjournalSpider(scrapy.Spider):
    name = 'jastjournal'
    allowed_domains = ['jast-journal.springeropen.com']
    start_urls = ['https://jast-journal.springeropen.com/articles']

    title_xpath = '//h1[@class="c-article-title"]/text()'
    author_xpath = '//a[@data-test="author-name"]/text()'
    contentdate_xpath = '//a[@data-track-action="publication date"]/time/text()'
    text_xpath = '//section[@data-title and parent::article]/descendant::text()'

    def parse(self, response):
        links = response.xpath('//a[@data-test="title-link"]')
        for l in links:
            yield response.follow(url=l, callback=self.parse_page)
        
        next_page = response.xpath('//a[@rel="next"]')
        if next_page:
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