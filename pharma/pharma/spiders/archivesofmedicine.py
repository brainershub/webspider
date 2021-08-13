# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from dateutil import parser
from datetime import datetime

from scrapy.utils.trackref import NoneType

class ArchivesofmedicineSpider(CrawlSpider):
    name = 'archivesofmedicine'
    allowed_domains = ['www.archivesofmedicine.com']
    start_urls = ['https://www.archivesofmedicine.com/current-issue.php']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h2/following-sibling::ul/li/p[last()]/a[@title="Full-Text"]'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//a[@rel="next"]'), callback='parse_item', follow=True),
    )

    title_xpath = '//div[@class="ft_top_content"]/h1/text()'
    text_xpath = '//div[@class="ft_below_content"]/descendant::text()[not(parent::li)]'
    author_xpath = '//dl[@class="dl-horizontal"]/dd/text()[not(preceding-sibling::strong)]'
    contentdate_xpath = '//dl[@class="dl-horizontal"]/following-sibling::p[last()-1]/text()[last()]'


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

def clean_date(date_raw):

    class GermanParserInfo(parser.parserinfo):
        MONTHS = [
            ('Jan', 'Januar', 'Jänner', 'January', 'Jan.'),
            ('Feb', 'Februar', 'February', 'Feb.'),
            ('Mär', 'Mrz', 'März', 'March'),
            ('Apr', 'April'),
            ('Mai', 'May'),
            ('Jun', 'Juni', 'June'),
            ('Jul', 'Juli', 'July'),
            ('Aug', 'August'),
            ('Sep', 'Sept', 'September'),
            ('Okt', 'Oktober', 'October', 'Oct.'),
            ('Nov', 'November'),
            ('Dez', 'Dezember', 'December', 'Dec.'),
        ]

    if date_raw == " von ":
        date_raw = datetime.today().strftime("%d-%m-%Y")
    elif type(date_raw) == NoneType:
        date_raw = datetime.today().strftime("%d-%m-%Y")

    date = date_raw.replace('/', '.')
    # date = parse(date)
    date = parser.parse(date, GermanParserInfo())
    date = date.strftime("%d-%m-%Y")
    date = datetime.strptime(date, '%d-%m-%Y')

    return date

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(ArchivesofmedicineSpider)
    process.start()