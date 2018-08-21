# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from scrapy import signals
from scrapy.exporters import CsvItemExporter


class JsonPipeline(object):
    def __init__(self):
        self.file = codecs.open('top250.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class CSVPipeline(CsvItemExporter):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        savefile = open('douban_top250_export.csv', 'wb+')
        self.files[spider] = savefile
        self.exporter = CsvItemExporter(savefile)
        self.exporter.fields_to_export = [
            'rank',
            'score',
            'title_CN',
            'title_EN',
            'url',
            'detail',
        ]
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        savefile = self.files.pop(spider)
        savefile.close()

    def process_item(self, item, spider):
        print(type(item))
        self.exporter.export_item(item)
        return item
