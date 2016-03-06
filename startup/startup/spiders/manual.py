# -*- coding: utf-8 -*-
import scrapy
import datetime
import urlparse
import socket
from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader
from startup.items import StartupItem
from scrapy.http import Request

class BasicSpider(scrapy.Spider):
    name = "manual"
    allowed_domains = ["web"]
    start_urls = (
        'http://tech.qq.com/',
    )

    def parse_item(self, response):

        l = ItemLoader(item=StartupItem(), response=response)
        l.add_xpath('title', '//*[@id="C-Main-Article-QQ"]//h1/text()')
        l.add_xpath('abstract', '//*[@id="C-Main-Article-QQ"]//p[@class="Introduction"]/text()',)

        # Housekeeping fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('scrapy_test'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())
        return l.load_item()

    def parse(self, response):

        # Get item URLs and yield Requests
        item_selector = response.xpath('//*[@id="listZone"]/div[1]//h3/a/@href')
        for url in item_selector.extract():
            yield Request(urlparse.urljoin(response.url, url),
                          callback=self.parse_item)