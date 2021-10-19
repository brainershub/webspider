import scrapy

class SciencedirectSpider(scrapy.Spider):
    name = 'sciencedirect'
    allowed_domains = ['www.sciencedirect.com']
    start_urls = ['https://www.sciencedirect.com/journal/reproduction-and-breeding/issues']

    title_xpath = '//span[@class="title-text"]/text()'
    text_xpath = '//*[contains(@id, "sec")]/descendant::text()'
    author_xpath = '//div[@id="author-group"]/a//text()[not(parent::sup)]'
    contentdate_xpath = '//div[@class="text-xs"]/text()[2]'

    def parse(self, response):
        links = response.xpath('//section[@class="js-issue-list-content"]//a')
        for link in links:
            yield response.follow(url=link, callback=self.parse_volumes)

    def parse_volumes(self, response):
        links = response.xpath('//h3/a')        
        for link in links:
            yield response.follow(url=link, callback=self.parse_item)


    def parse_item(self, response):
        author_list = response.xpath(self.author_xpath).getall()
        authors = ', '.join(author_list)
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        content_date_raw = response.xpath(self.contentdate_xpath).get()
        content_date_clean = "1. " + content_date_raw 

        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': authors,
            'content_text': text,
            'content_date': content_date_clean,
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }
