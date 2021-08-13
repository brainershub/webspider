from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pharma.features import clean_date

class KnepublishingSpider(CrawlSpider):
    name = 'knepublishing'
    allowed_domains = ['knepublishing.com']
    start_urls = ['https://knepublishing.com/index.php/KnE-Materials',
    'https://knepublishing.com/index.php/KnE-Social',
    'https://knepublishing.com/index.php/KnE-Energy',
    'https://knepublishing.com/index.php/KnE-Engineering',
    'https://knepublishing.com/index.php/KnE-Life',
    'https://knepublishing.com/index.php/KnE-Medicine'
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="item-container"]/a[1]'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//ul[@class="pagination pull-right"]/li[1]/a'), follow=True),
    )

    title_xpath = '//h2[@id="abstract"]/text()'
    text_xpath = '//div[@class="author"]/following-sibling::p/descendant::text()'
    author_xpath = '//section[@class="article-outer"]//h3[text()="authors"]/following-sibling::ul[1]/li/a/text()'
    contentdate_xpath = '//section[@class="article-outer"]//h3[text()="Published Date"]/following-sibling::ul/li/text()'


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

