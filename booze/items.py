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
    # TODO, add UPC, Alcohol %, and size of bottle in mL
    # upc = scrapy.Field()
