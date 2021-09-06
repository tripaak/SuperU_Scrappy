# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CoursesuItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    address = scrapy.Field()
    postalcode = scrapy.Field()
    city = scrapy.Field()
    Drive = scrapy.Field()
    Livraison = scrapy.Field()
    
