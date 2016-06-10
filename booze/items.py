# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BoozeItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    volume = scrapy.Field()
    sale = scrapy.Field()
    savings = scrapy.Field()
    # TODO, add Category of booze, Alcohol %, UPC, etc.
    # upc = scrapy.Field()
