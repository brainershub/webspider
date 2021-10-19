import scrapy
from scrapy_splash import SplashRequest

class OmicsonlineSpider(scrapy.Spider):
    name = 'omicsonline'
    allowed_domains = ['www.omicsonline.org']
    start_urls = ['https://www.omicsonline.org/latest-research-reports.php']

    title_xpath = '//h1/text()'
    text_xpath = '//dl[@class="authors"]/following-sibling::div/descendant::text()'
    author_xpath = '//dl[@class="authors"]//a/@title'
    contentdate_xpath = 'substring-after(//article[@class="full-text"]/div[@class="mb-1"]/p/em/text(), "Published Date:")'

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

    def parse(self, response):
        links = response.xpath('//a[contains(text(),"Full Text")]')
        for l in links:
            yield response.follow(url=l, callback=self.parse_page)

    def parse_page(self, response):
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
