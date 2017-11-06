# encoding=UTF-8
from lxml import etree
from collections import OrderedDict
import re
from pprint import pprint
import arrow


class Parser:
    def __init__(self):
        self.links = set()
        self.items = []

    def parse_list(self, tree):
        houses_select = '//ul[@id="house-lst"]/li'
        houses_lst = tree.xpath(houses_select)
        for house_box in houses_lst:
            item = OrderedDict()
            link = house_box.xpath('./div[@class="info-panel"]/h2/a/@href')[0]
            item['link'] = link
            self.links.add(link)

            item['title'] = house_box.xpath('./div[@class="info-panel"]/h2/a/text()')[0].strip()
            if house_box.xpath('.//span[@class="region"]/text()'):
                item['compound'] = house_box.xpath('.//span[@class="region"]/text()')[0].strip()
            else:
                item['compound'] = None
            if house_box.xpath('.//span[@class="zone"]/span/text()'):
                item['layout'] = house_box.xpath('.//span[@class="zone"]/span/text()')[0].strip()
            else:
                item['layout'] = None
            if house_box.xpath('.//span[@class="meters"]/text()'):
                item['gross_floor_area'] = house_box.xpath('.//span[@class="meters"]/text()')[0].strip()
            else:
                item['gross_floor_area'] = None
            con_select = './/div[@class="con"]//text()'
            con_text = house_box.xpath(con_select)
            item['distribute'] = con_text[0]
            item['floor'] = con_text[2]
            if len(con_text) > 4:
                item['structure'] = con_text[4]
            else:
                item['structure'] = None
            if house_box.xpath('.//div[@class="where"]/span[not(@class)]/text()'):
                item['orientation'] = house_box.xpath('.//div[@class="where"]/span[not(@class)]/text()')[0].strip()
            else:
                item['orientation'] = None

            item['rent_per_month'] = house_box.xpath('.//div[@class="price"]/span/text()')[0].strip()
            item['added_at'] = house_box.xpath('.//div[@class="price-pre"]/text()')[0].strip()[:-3]
            item['total_views'] = house_box.xpath('.//div[@class="square"]/div/span[@class="num"]/text()')[0].strip()

            subway_select = './/span[@class="fang-subway-ex"]/span/text()'
            subway_text = house_box.xpath(subway_select)
            if subway_text:
                subway_pattern = r'距离([0-9]{1,2})号线(\w+)站([0-9]+)米'
                subway_text = subway_text[0]
                g = re.match(subway_pattern, subway_text)
                if g:
                    item['subway_line'] = g.groups()[0]
                    item['subway_station'] = g.groups()[1]
                    item['subway_distance'] = g.groups()[2]
            else:
                item['subway_line'] = None
                item['subway_station'] = None
                item['subway_distance'] = None

            item['captured_date'] = arrow.now().format('YYYY-MM-DD')

            self.items.append(item)

        return self.items, self.links

    def parse_detail(self, tree, item):
        pass
