import scrapy
from Term_Project_2022.items import TermProject2022Item
from Term_Project_2022.middlewares import TermProject2022DownloaderMiddleware
import time
from datetime import datetime


class mySpider(scrapy.spiders.Spider):
    name = "XIDIAN_JIUYE_ALL"
    allowed_domains = ["job.xidian.edu.cn"]
    start_urls = ["https://job.xidian.edu.cn/campus/index?do=&domain=xidian&city=&page=1"]
    # 存储下一页的url
    xidian_next_page = ''

    # 解析爬取的内容
    def parse(self, response):
        item = TermProject2022Item()
        next_page_href = response.css('li[class="next"]>a::attr(href)').extract()
        # 当处于最后一页时下一页就是当前已选择的页面
        selected_page_href = response.css('li[class="page selected"]>a::attr(href)').extract()
        if next_page_href != selected_page_href:
            self.xidian_next_page = 'https://job.xidian.edu.cn' + next_page_href[0]
        else:
            self.xidian_next_page = ''

        # 获取每个详情页的url
        c_page_url_list = response.css('ul[class="infoList"]>li:nth-child(1)>a')
        for job in c_page_url_list:
            driver = TermProject2022DownloaderMiddleware.get_XIDIAN_driver()
            # 获取driver打开详情页
            driver.get('https://job.xidian.edu.cn' + job.css('a::attr(href)').extract()[0])
            time.sleep(1)
            # 找到标题
            item['job_title'] = [driver.find_element('css selector', 'div[class="title-message"]>h5').text]
            # 找到时间并去除多余文字
            date_text = driver.find_element('css selector', 'div[class="share"]>ul>li:nth-child(1)').text
            date_text = date_text[date_text.find('：') + 1:]
            # 如果时间在十月一号之前就直接退出爬虫
            if datetime.strptime(date_text, '%Y-%m-%d %H:%M') < datetime.strptime('2022-10-01 00:00', '%Y-%m-%d %H:%M'):
                self.xidian_next_page = ''
                break
            item['job_date'] = [date_text]
            # 获取浏览量并去除多余文字
            views_text = driver.find_element('css selector', 'div[class="share"]>ul>li:nth-child(2)').text
            item['job_views'] = [views_text[views_text.find('：') + 1:]]
            yield item
        # 如果没到最后一页,在处理完这一页后转到下一页
        if self.xidian_next_page != '':
            yield scrapy.Request(url=self.xidian_next_page, callback=self.parse)
