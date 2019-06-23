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
import pymongo


class Pipelines(object):
    def __init__(self):
        # Connect to database
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # If having username and password
        self.client.admin.authenticate(settings['MONGO_USER'],settings['MONGO_PSW'])
        self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        self.coll = self.db[settings['MONGO_COLL']]  # 获得Collection的句柄

    def process_items(self, item, spider):
        try:
            title = item['title'][0]
            link = item['link']
            price = item['price'][0]
            now_price = item['now_price']
            comment = item['comment'][0]
            address = item['address']

            # Print out the information
            print('Product Title\t', title)
            print('Product Link\t', link)
            print('Original Price\t', price)
            print('Current Price\t', now_price)
            print('Shop Address\t', address)
            print('Number of Comments\t', comment)
            print('---------------------------------------------\n')

            # Post the information to data base
            postItem = dict(Product_Title=title,
                            Prodcut_Link=link,
                            Original_Price=price,
                            Current_Price=now_price,
                            Shop_Address=address,
                            NUmber_of_Comments=comment)
            self.coll.insert(postItem)
            return item
        # Handle Errors
        except Exception as err:
            pass
        pass
