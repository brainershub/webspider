import scrapy


class HumupdSpider(scrapy.Spider):
    name = 'humupd'
    allowed_domains = ['academic.oup.com']
    start_urls = ['https://academic.oup.com/humupd/issue-archive']

    title_xpath = '//h1/text()'
    text_xpath = '//div[@class="widget-items"]/descendant::text()'
    author_xpath = '//a[@class="linked-name js-linked-name-trigger"]/text()'
    contentdate_xpath = '//div[@class="citation-date"]/text()'

    def parse(self, response):
        links = response.xpath('//section[@class="master-main row"]/div/div/div/div/a')
        for link in links:
            yield response.follow(url=link, callback=self.parse_volumes)

    def parse_volumes(self, response):
        links = response.xpath('//div[@class="customLink"]/a')
        
        for link in links:
            yield response.follow(url=link, callback=self.parse_articles_listing)

    def parse_articles_listing(self, response):
        links = response.xpath('//h5[@class="customLink item-title"]/a')
        for link in links:
            yield response.follow(url=link, callback=self.parse_item)


    def parse_item(self, response):
        author_list = response.xpath(self.author_xpath).getall()
        authors = ', '.join(author_list)
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)


        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': authors,
            'content_text': text,
            'content_date': response.xpath(self.contentdate_xpath).get(),
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }
