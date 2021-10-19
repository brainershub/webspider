import scrapy
from scrapy_splash import SplashRequest


class LaekhSpider(scrapy.Spider):
    name = 'laekh'
    allowed_domains = ['www.laekh.de']
    start_urls = ['https://www.laekh.de/aktuelles', 'https://www.laekh.de/presse/pressemitteilungen']

    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'

    title_xpath = '//h1/text()'
    text_xpath = '//*[@itemprop="articleBody"]/descendant::text()'
    author_xpath = '//span[@class="autoren"]/text()'
    contentdate_xpath = 'substring-after(//div[@class="row-fluid" and preceding-sibling::h2]/div[contains(@class, "details")]/p[1]/text()[last()], ": ")'

    script = '''
    function main(splash, args)
        splash.private_mode_enabled = false
        url = args.url
        assert(splash:go(url))
        assert(splash:wait(1))
        splash:set_viewport_full()
        return splash:html()
    end
    '''

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    # def set_user_agent(self, request):
    #     request.headers['User-Agent'] = self.user_agent
    #     return request

    def parse(self, response):
        links = response.xpath('//h2/parent::a')
        for link in links:
            yield response.follow(url=link, callback=self.parse_article, meta={'date':link.xpath('.//time/text()').get()})
        
    def parse_article(self, response):
        # author_list = response.xpath(self.author_xpath).getall()
        # authors = ', '.join(author_list)

        text_list = response.xpath(self.text_xpath).getall()
        for el in text_list:
            el = el.strip()
        text = '\n'.join(text_list)

        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': 'Landesärztekammer Hessen',
            'content_text': text,
            'content_date': response.meta.get('date'),
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'aerztekammer'
        }
