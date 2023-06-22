import scrapy
from Term_Project_2022.items import TermProject2022Item
from Term_Project_2022.middlewares import TermProject2022DownloaderMiddleware
import time
from datetime import datetime


class mySpider(scrapy.spiders.Spider):
    name = "BEIYOU_JIUYE_ALL"
    allowed_domains = ["job.bupt.edu.cn"]
    start_urls = ["https://job.bupt.edu.cn/frontpage/bupt/html/recruitmentinfoList.html?type=1&"]

    # 解析爬取的内容
    def parse(self, response):
        item = TermProject2022Item()
        current_page = 1
        # 获取招聘网站的最大页数，为倒数第二个li，即下一页之前的元素
        max_page = int(response.css('ul[class="fPage"]>li:nth-last-child(2)>a::text').extract()[0])
        # 因为北邮就业网站点击下一页时没有跳转url，所以直接使用driver打开网页
        driver = TermProject2022DownloaderMiddleware.get_BEIYOU_driver()
        driver.get('https://job.bupt.edu.cn/frontpage/bupt/html/recruitmentinfoList.html?type=1&')
        time.sleep(1)
        # 通过F12检查发现，北邮就业网站切换页面实际上是调用page(i,15,'')函数，其中i为跳转到第几页，所以直接通过driver执行js语句进入第一页
        driver.execute_script(f"page({current_page},15,'')")
        time.sleep(1)
        # 一直找直到最后一页或时间早于十月一日
        while True:
            # c_page_url_list = response.css('div[class="left"]>a')
            # 通过driver获取工作列表
            c_page_url_list = driver.find_elements('css selector', 'div[class="left"]>a')
            c_page_url_list = [i.get_attribute("href") for i in c_page_url_list]
            for job in c_page_url_list:
                # 用driver打开详情页
                driver.get(job)
                time.sleep(1)
                # 找到标题
                item['job_title'] = [driver.find_element('css selector', 'div[class="name getCompany"]').text]
                # 找到时间和浏览次数
                text = driver.find_element('css selector', 'div[class="midInfo"]>div[class="l_con"]').text
                # 分离出时间
                date_text = text[text.find('日期：') + 3:text.find('日期：') + 13]
                # 如果时间在十月一号之前就直接退出爬虫
                if datetime.strptime(date_text, '%Y-%m-%d') < datetime.strptime('2022-10-01', '%Y-%m-%d'):
                    # 设置当前页面为最大页面，在后续代码中可直接退出while循环
                    current_page = max_page
                    break
                item['job_date'] = [date_text]
                # 分离出浏览量
                item['job_views'] = [text[text.find('次数：') + 3:]]
                yield item

            # 如果当前页面就是最大页面，说明已经到达最后一页或工作发布时间早于十月一日，直接退出循环
            if current_page == max_page:
                break
            # 进入下一页
            current_page = current_page + 1
            driver.get(self.start_urls[0])
            driver.execute_script(f"page({current_page},15,'')")
            time.sleep(2)