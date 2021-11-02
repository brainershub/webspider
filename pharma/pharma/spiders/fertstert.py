from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class FertstertSpider(CrawlSpider):
    name = 'fertstert'
    allowed_domains = ['www.fertstert.org']
    start_urls = ['https://www.fertstert.org/inpress']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[text()="Full-Text HTML"]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[@title="Next page"]'), follow=True),
    )

    title_xpath = '//h1/text()'
    text_xpath = '//div[@class="section-paragraph"]/descendant::text()'
    author_xpath = '//li[@class="loa__item author"]/div/a/text()'
    contentdate_xpath = '//span[@class="article-header__publish-date__value"]/text()'


    def parse_item(self, response):
        author_list = response.xpath(self.author_xpath).getall()
        authors = ', '.join(author_list)
        text_list = response.xpath(self.text_xpath).getall()
        text = '\n'.join(text_list)
        content_date_raw = response.xpath(self.contentdate_xpath).get()
        content_date_clean = clean_date(content_date_raw)

        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': authors,
            'content_text': text,
            'content_date': content_date_clean,
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }

