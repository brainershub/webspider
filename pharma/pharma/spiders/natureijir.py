import scrapy

class NatureijirSpider(scrapy.Spider):
    name = 'natureijir'
    allowed_domains = ['www.nature.com']
    start_urls = ['https://www.nature.com/ijir/volumes']

    title_xpath = '//h1/text()'
    author_xpath = '//a[@data-test="author-name"]/text()'
    # contentdate_xpath = '//span[@class="article-published"]/span/text()'
    text_xpath = '//div[@class="c-article-body"]/descendant::text()[parent::p or parent::h2]'

    

    def parse(self, response):
        volumes = response.xpath('//ul[@id="volume-decade-list"]/li/a')
        for v in volumes:
            yield response.follow(url=v, callback=self.parse_issues)

    def parse_issues(self, response):
        issues = response.xpath('//ul[@id="issue-list"]/li/a')
        for i in issues:
            yield response.follow(url=i, callback=self.parse_issue)

    def parse_issue(self, response):
        articles = response.xpath('//article')
        for a in articles:
            href = a.xpath('.//a[@data-track-action="view article"]/@href').get()
            url = response.urljoin(href)
            date = a.xpath('.//time/text()').get()
            yield response.follow(url=url, callback=self.parse_page, meta={'date': date})

    def parse_page(self, response):
        author_list = response.xpath(self.author_xpath).getall()
        authors = ', '.join(author_list)
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        content_date_raw = response.meta.get('date')
        
        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': authors,
            'content_text': text,
            'content_date': content_date_raw,
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }
