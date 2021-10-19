import scrapy


class IefSpider(scrapy.Spider):
    name = 'ief'
    allowed_domains = ['www.ief.at']
    start_url = ['https://www.ief.at/politik']

    title_xpath = '//h1/text()'
    # author_xpath = '//h1[@class="entry-title"]/following-sibling::span[@class="author-links"]/span[last()]/a/text()'
    contentdate_xpath = 'substring-before(substring-after(//div[@class="fusion-text fusion-text-1"]/p[1]/text(), "IEF,"), "–")'
    text_xpath = '//div[@class="fusion-content-tb fusion-content-tb-1"]/descendant::text()'

    def parse(self, response):
        links = response.xpath('//h2[@class="blog-shortcode-post-title"]/a')
        for l in links:
            yield response.follow(url=l, callback=self.parse_page)
        
        next_page = response.xpath('//a[@class="pagination-next"]')
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse)
        

    def parse_page(self, response):
        # author_list = response.xpath(self.author_xpath).getall()
        # authors = ', '.join(author_list)
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        content_date_raw = response.xpath(self.contentdate_xpath).get()
        
        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': 'IEF',
            'content_text': text,
            'content_date': content_date_raw,
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'news'
        }