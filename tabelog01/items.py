# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Tabelog01Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Restaurant(scrapy.Item):
    """
    食べログのレストラン情報
    """
    url = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    station = scrapy.Field()
    transportation = scrapy.Field()
    genre = scrapy.Field()
    score = scrapy.Field()