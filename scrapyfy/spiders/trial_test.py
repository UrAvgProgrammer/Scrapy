import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapyfy.items import ScrapyfyItem
import re

class MySpider(CrawlSpider):
   name = '###'
   allowed_domains = ['####']
   start_urls = ['###']

   rules = (
      #select all link with allowed domains except for /afterpay
      Rule(LinkExtractor(unique=True, deny=('/afterpay'), ), callback='parse_item', follow=True),
   )

   def parse_item(self, response):
      item = ScrapyfyItem()

      #extracting categories from search-result?
      categories = response.css('head link::attr(href)').extract_first()

      #transforming into list using split
      category = re.split('=|&', categories)
      #to clean the category replacing the %20 and - into white spaces
      category = list(map(lambda x: x.replace('%20',' ').replace('-',' '),category))

      for information in response.css('div.product'):
         
         #a simple checking to see if the code catches empty reponses
         if information.css('div.product_content h2.product_content_name::text').extract_first():
               item['product_name'] = information.css('div.product_content h2.product_content_name::text').extract_first()
               item['brand'] = information.css('div.product_content span.product_content_brand::text').extract_first()
               item['image_links'] =  information.css('div.product_image img::attr(src)').extract_first()

               #Check if it is discounted price if true then use the css selector below
               if information.css('div.product_content span.product_content_price.price span.price_discount::text').extract_first():
                  item['price'] = information.css('div.product_content span.product_content_price.price span.price_discount::text').extract_first()
                  item['sale_price'] = information.css('div.product_content span.product_content_price.price span.price_strikethrough::text').extract_first()
               else:
                  item['price'] = information.css('div.product_content span.product_content_price.price::text').extract_first()
                  item['sale_price'] = ''

               #to fix categories where data at list category[3] is store instead of the sub category value
               if category[3] == 'store':
                  item['category'] = category[1] + " >> " + category[5]
               else:
                  item['category'] = category[1] + " >> " + category[3]
               yield item
