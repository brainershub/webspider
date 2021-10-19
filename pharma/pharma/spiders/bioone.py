import scrapy

class BiooneSpider(scrapy.Spider):
    name = 'bioone'
    allowed_domains = ['bioone.org']
    start_urls = ['https://bioone.org/journals/biology-of-reproduction/current']

    title_xpath = '//text[@class="ProceedingsArticleOpenAccessHeaderText"]/text()'
    text_xpath = '//*[@id="divARTICLECONTENTTop"]/descendant::text()'
    author_xpath = '//text[@class="ProceedingsArticleOpenAccessText"]/span/text()'
    contentdate_xpath = '//text[@class="DetailDate"]/text()'

    def parse(self, response):
        links = response.xpath('//div[@class="TOCLineItemRowCol1"]//a[@class="TocLineItemAnchorText1"]')
        for link in links:
            yield response.follow(url=link, callback=self.parse_item)

            # img = a.xpath('//img')
            # if img is not None:
            #     url = a.xpath('//a[@class="TocLineItemAnchorText1"]')
            #     if isinstance(url, scrapy.selector.SelectorList):
            #         yield response.follow(url=url[0], callback=self.parse_item)
            #     else:    
            #         yield response.follow(url=url, callback=self.parse_item)
            # else:
            #     pass


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
            'content_date': response.xpath(self.contentdate_xpath).get(),
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }