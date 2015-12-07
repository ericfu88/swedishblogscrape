# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SwedishblogArticle(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    publishDate = scrapy.Field()
    author = scrapy.Field()
    contents = scrapy.Field()
    topics = scrapy.Field()
