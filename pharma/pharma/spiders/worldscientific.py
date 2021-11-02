import scrapy

class WorldscientigicSpider(scrapy.Spider):
    name = 'worldscientific'
    allowed_domains = ['www.worldscientific.com']
    start_urls = ['https://www.worldscientific.com/action/showNews']

    title_xpath = '//h1/text()'
    # author_xpath = '//a[@data-test="author-name"]/text()'
    contentdate_xpath = '//div[@class="news__date"]/span[last()]/text()'
    text_xpath = '//div[@class="news__body"]/descendant::text()'

    def parse(self, response):
        links = response.xpath('//a[@class="news-list_item_title"]')
        for l in links:
            yield response.follow(url=l, callback=self.parse_page)
        

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
            'author': 'Worldsientific',
            'content_text': text,
            'content_date': content_date_raw,
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'news'
        }