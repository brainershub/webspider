import scrapy


class JriSpider(scrapy.Spider):
    name = 'jri'
    allowed_domains = ['www.jri.ir']
    start_urls = ['https://www.jri.ir/en/archive']

    title_xpath = '//h1/text()'
    text_xpath = '//div[@class="mgt10"]/descendant::text()'
    author_xpath = '//div[@class="text-left"]//dt//text()'
    contentdate_xpath = '//div[@class="text-xs"]/text()[2]'

    def parse(self, response):
        links = response.xpath('//div[@class="tab-content"]//a[not(child::img)]')
        for link in links:
            yield response.follow(url=link, callback=self.parse_volumes)

    def parse_volumes(self, response):
        links = response.xpath('//a[@class="list-group-item"]')
        date = "1. " + response.xpath('substring-after(//h1/small/text(), "-")').get()
        for link in links:
            yield response.follow(url=link, callback=self.parse_item, meta={'date': date})


    def parse_item(self, response):
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
