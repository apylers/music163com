# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Music163ComItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    playlist_title = scrapy.Field()
    _id = scrapy.Field()
    name = scrapy.Field()
    time = scrapy.Field()
    artists = scrapy.Field()
    album = scrapy.Field()
