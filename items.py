# -*- coding: utf-8 -*-
"""
 -------------------------------------------------------------------
    File Name: 
    Description: 
    Author: Yuxiang Chen
    Date: 
 -------------------------------------------------------------------
    Change Activity:
    
 -------------------------------------------------------------------
 """
import scrapy


class TaobaoSpiderItem(scrapy.Item):
    # define the fields for your item here:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    comment = scrapy.Field()
    now_price = scrapy.Field()
    address = scrapy.Field()
    pass


