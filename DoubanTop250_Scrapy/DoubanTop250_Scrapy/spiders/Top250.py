# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from DoubanTop250_Scrapy.items import DoubanTop250Item


class Top250Spider(scrapy.Spider):
    name = 'Top250'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        data = response.xpath('//div[@class="item"]')
        for movie in data:
            item = DoubanTop250Item()
            item['rank'] = movie.xpath('.//em/text()').extract_first()
            item['title_CN'] = movie.xpath('.//span[@class="title"][1]/text()').extract_first()
            title_en = movie.xpath('.//span[@class="title"][2]/text()').extract_first()
            if title_en is not None:
                item['title_EN'] = title_en.replace("\xa0/\xa0", "")
            item['score'] = movie.xpath('.//span[@class="rating_num"]/text()').extract_first()
            item['url'] = movie.xpath('.//div[@class="hd"]/a/@href').extract_first()
            item['detail'] = movie.xpath('.//div[@class="bd"]/p/text()').extract_first().replace("\n", "")
            yield item

        next_page_url = response.xpath('//span[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            next_page_url = 'https://movie.douban.com/top250' + next_page_url
            yield Request(next_page_url)
