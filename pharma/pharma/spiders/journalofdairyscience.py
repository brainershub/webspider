import scrapy

class JournalofdairyscienceSpider(scrapy.Spider):
    name = 'journalofdairyscience'
    allowed_domains = ['www.journalofdairyscience.org']
    start_urls = ['https://www.journalofdairyscience.org/issues']


    title_xpath = '//h1/text()'
    text_xpath = '//div[@class="section-paragraph"]/descendant::text()'
    author_xpath = '//li[@class="loa__item author"]//a/text()'
    contentdate_xpath = '//span[@class="article-header__publish-date__value"]/text()'


    def parse(self, response):
        volumes = response.xpath('//ul[@class="rlist"]//li[not(@class)]/a')
        for volume in volumes:
            yield response.follow(url=volume, callback=self.parse_volume)


    def parse_volume(self, response):
        articles = response.xpath('//a[text()="Full-Text HTML"]')
        next_page = response.xpath('//a[@title="Next page"]')

        for article in articles:
            yield response.follow(url=article, callback=self.parse_article)

        if next_page:
            yield response.follow(url=next_page, callback=self.parse_volume)


    def parse_article(self, response):
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