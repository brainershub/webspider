# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PharmaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    title = scrapy.Field()
    author = scrapy.Field()
    content_text = scrapy.Field()
    content_date = scrapy.Field()
    url = scrapy.Field()
    url_base = scrapy.Field()
    labels = scrapy.Field()
    
