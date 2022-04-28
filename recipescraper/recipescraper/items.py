# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RecipescraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    instructions = scrapy.Field()
    ingredients = scrapy.Field()
