from scrapy import Spider

class MedwissSpider(Spider):
    name = 'medwiss'
    allowed_domains = ['www.medwiss.de']
    start_urls = ['https://www.medwiss.de/krankheitsbilder/fertilitaet',
                    # 'https://www.medwiss.de/krankheitsbilder/pco-syndrom',
                    'https://www.medwiss.de/krankheitsbilder/endometriose'
    ]

    title_xpath = '//article/h1/text()'
    author_xpath = '//a[@title="Link zum originalen Abstract"]/text()'
    contentdate_xpath = '//li[@class="date"]/small/text()'
    text_xpath = '//article/descendant::text()[not(ancestor::script)]'

    def parse(self, response):
        links = response.xpath('//h3[@class="post-title"]/a')
        for l in links:
            yield response.follow(url=l, callback=self.parse_page)
        
        # next_page = response.xpath('//div[@id="sort-results"]/following-sibling::form/a[@class="next"]/@href')
        # if next_page is not None:
        #     if next_page is SelectorList:
        #         yield response.follow(url=next_page[0], callback=self.parse)
        #     else:
        #         yield response.follow(url=next_page, callback=self.parse)
        

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
            'labels': 'news'
        }