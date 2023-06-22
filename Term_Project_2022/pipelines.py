# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv


class TermProject2022Pipeline:
    # 把获取的数据写入文件
    def process_item(self, item, spider):
        try:
            dict_item = dict(item)
            if spider.name == 'XIDIAN_JIUYE_ALL':
                self.XIDIAN_writer.writerow(dict_item)
            else:
                self.BEIYOU_writer.writerow(dict_item)
                # self.BEIYOU_file.flush()
            return item
        except Exception as e:
            print(e)

    def open_spider(self, spider):
        if spider.name == 'XIDIAN_JIUYE_ALL':
            self.XIDIAN_file = open('XIDIAN_1.csv', "w+", newline='', encoding='utf-8')
            self.XIDIAN_writer = csv.DictWriter(self.XIDIAN_file, fieldnames=['job_title', 'job_date', 'job_views'])
            self.XIDIAN_writer.writeheader()
        else:
            self.BEIYOU_file = open('BEIYOU_1.csv', "w+", newline='', encoding='utf-8')
            self.BEIYOU_writer = csv.DictWriter(self.BEIYOU_file, fieldnames=['job_title', 'job_date', 'job_views'])
            self.BEIYOU_writer.writeheader()

    def close_spider(self, spider):
        if spider.name == 'XIDIAN_JIUYE_ALL':
            self.XIDIAN_file.close()
        else:
            self.BEIYOU_file.close()
