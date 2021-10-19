import scrapy


class AcademicSpider(scrapy.Spider):
    name = 'academic'
    allowed_domains = ['academic.oup.com']
    start_urls = [
                # 'https://academic.oup.com/biolreprod/issue-archive',
                # 'https://academic.oup.com/humrep/issue-archive',
                # 'https://academic.oup.com/hropen/issue-archive',
                # 'https://academic.oup.com/molehr/issue-archive'
                'https://academic.oup.com/biolreprod',
                'https://academic.oup.com/humrep',
                'https://academic.oup.com/hropen',
                'https://academic.oup.com/molehr'
                ]

    title_xpath = '//h1/text()'
    text_xpath = '//p[@class="chapter-para"]/descendant::text() |//div[@class="title"] | //div[@class="widget-items"]//h5/text() | //div[@class="widget-items"]//h2/text()'
    author_xpath = '//a[@class="linked-name js-linked-name-trigger"]/text()'
    contentdate_xpath = '//div[@class="citation-date"]/text()'

    # def parse(self, response):
    #     links = response.xpath('//section[@class="master-main row"]/div/div/div/div/a')
        
    #     if not links:
    #         self.parse_articles_listing(response)
        
    #     for link in links:
    #         yield response.follow(url=link, callback=self.parse_volumes)

    # def parse_volumes(self, response):
    #     links = response.xpath('//div[@class="customLink"]/a')
        
    #     for link in links:
    #         yield response.follow(url=link, callback=self.parse_articles_listing)

    # def parse_articles_listing(self, response):
    #     links = response.xpath('//h5[@class="customLink item-title"]/a')
    #     for link in links:
    #         yield response.follow(url=link, callback=self.parse_item)

    def parse(self, response):
        links = response.xpath('//a[child::div[contains(@class, "title")]]')
        for link in links:
            yield response.follow(url=link, callback=self.parse_item)

    def parse_item(self, response):
        author_list = response.xpath(self.author_xpath).getall()
        # if author_list:
        #     authors = author_list
        # else:
        #     authors = 'None'
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
