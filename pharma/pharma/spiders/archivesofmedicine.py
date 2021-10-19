# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


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

        yield {
            'title': response.xpath(self.title_xpath).get(),
            'author': authors,
            'content_text': text,
            'content_date': content_date_raw,
            'url': response.url,
            'url_base': self.allowed_domains[0],
            'labels': 'journal'
        }


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(ArchivesofmedicineSpider)
    process.start()