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
import re
from scrapy.http import Request
from items import TaobaoSpiderItem
import urllib.request


class taobao_spider(scrapy.Spider):

    allow_domains = [""]
    initial_urls = [""]

    # Map input to urls to be crawled
    # Request the website url to be crawled
    def parse(self, response):
        key = input("Enter Key Words: \t")
        pages = input("Enter Number of Pages to Craw: \t")
        print("\n")
        print("Current key words is:", key)
        print("\n")
        for i in range(0, int(pages)):
            url = "https://s.taobao.com/search?q=" + str(key) + "&s=" +str(44*i)
            # Work on this later
            yield Request(url=url, callback=self.page)

    # Request useful information from the search page for specific items
    def page(self, response):
        body = response.body.decode('utf-8', 'ignore')  # Figure out what the second parameter does

        # Use Regular Expression to extract information from html source code
        # The following regular expressions are subjected to change corresponding to the change in html source code
        pat_id = '"nid":"(.*?)"'  # match id
        pat_now_price = '"view_price":"(.*?)"'  # match price
        pat_address = '"item_loc":"(.*?)"'  # match address
        pat_sales = '"view_sales":"(.*?)人付款"'  # match sales

        all_id = re.compile(pat_id).findall(body)
        all_now_price = re.compile(pat_now_price).findall(body)
        all_address = re.compile(pat_address).findall(body)
        all_sales = re.compile(pat_sales).findall(body)

        for i in range(0, len(all_id)):
            this_id = all_id[i]
            now_price = all_now_price[i]
            address = all_address[i]
            sales = all_sales[i]
            url = "https://item.taobao.com/item/htm?id=" + str(this_id)
            yield Request(
                url=url,
                callback=self.next,
                meta={'now_price': now_price,
                      'address': address,
                      'sales': sales})

    # Request useful information from the shop page
    def next(self, response):
        item = TaobaoSpiderItem()
        url = response.url
        pat_url = "https://(.*?).com"
        # Get all the urls for shop page from the search page
        web = re.compile(pat_url).findall(url)
        print(web)  # Check to see what does this look like

        # Taobao and Tmall use different Ajax to load the pages
        # For Tmall
        if web[0] != 'item.taobao': # Check why is it web[0]
            title = response.xpath("//div[@class = 'tb-detail-hd']/h1/text()").extract()  # extract product name
            price = response.xpath("//span[@class = 'tm-price']/text()").extract()  # extract product price
            # can add more fields

            pat_id = 'id=(.*?)&'
            this_id = re.compile(pat_id).findall(url)[0]
        # For Taobao
        else:
            title = response.xpath("//h3[@class = 'tb-main-title']/@data-title").extract()  # extract product name
            price = response.xpath("//em[@class = 'tb-rmb-num']/text()").extract()  # extract product price
            # can add more fields

            pat_id = 'id=(.*?)&'
            this_id = re.compile(pat_id).findall(url)[0]

        # Get Total number of comments:
        comment_url = "https://rate.taobao.com/detailCount.do?callback=jsonp144&itemId=" + str(this_id)
        comment_data = urllib.request.urlopen(comment_url).read().decode('utf-8', 'ignore')
        each_comment = '"count":(.*?)}'
        comment = re.compile(each_comment).findall(comment_data)

        item['title'] =title
        item['link'] = url
        item['price'] = price
        item['now_price'] = response.meta['now_price']
        item['comment'] = comment
        item['address'] = response.meta['address']

        yield item  # Check the difference between yield and return !!!




