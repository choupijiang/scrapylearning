# -*- coding: utf-8 -*-
import scrapy
import datetime
import urlparse
import socket
from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader
from startup.items import StartupItem

class BasicSpider(scrapy.Spider):
    name = "basic"
    allowed_domains = ["web"]
    start_urls = (
        'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.4.ePvwFz&id=37657954084&skuId=97604772520&areaId=110100&cat_id=2&rn=3e1b21da991961fbe5078c747099bc00&user_id=1035986866&is_b=1',
    )

    def parse(self, response):

        l = ItemLoader(item=StartupItem(), response=response)
        l.add_xpath('name', '//*[@id="J_DetailMeta"]//h1/text()', MapCompose(unicode.strip))
        l.add_xpath('price', '//*[@id="J_StrPriceModBox"]/dd/span/text()', MapCompose(lambda i: i.replace('[', ''), float))
        l.add_xpath('image_urls', '//*[@id="J_ImgBooth"]/@src', MapCompose( lambda i: urlparse.urljoin(response.url, i)))
        # Housekeeping fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('scrapy_test'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        # l.add_value('date', datetime.datetime.now())

        # self.log("name: %s" % response.xpath(  '//*[@id="J_DetailMeta"]//h1/text()').extract())
        # self.log("price: %s" % response.xpath('//*[@id="J_StrPriceModBox"]/dd/span/text()').extract())
        # self.log("imgae: %s" % response.xpath('//*[@id="J_ImgBooth"]/@src').extract())
        return l.load_item()