# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ScrapyfyItem(Item):
   # Primary fields
   product_name = Field()
   brand = Field()
   category = Field()
   image_links = Field()
   price = Field()
   sale_price = Field()
