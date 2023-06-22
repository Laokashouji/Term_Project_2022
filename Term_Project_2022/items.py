# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TermProject2022Item(scrapy.Item):
    job_title = scrapy.Field()
    job_date = scrapy.Field()
    job_views = scrapy.Field()
