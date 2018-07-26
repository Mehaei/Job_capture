import scrapy
import datetime
from scrapy_project.items import JobsItem
import time
class LiePinSpider(scrapy.Spider):
    name = "liepin"
    start_urls = ['https://www.liepin.com/zhaopin/']

    custom_settings = {
        "CONCURRENT_REQUESTS":32,
        "ITEM_PIPELINES" : {
           'scrapy_project.pipelines.MysqlPipeline': 1,
        },
        "DEFAULT_REQUEST_HEADERS" : {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Cookie": "abtest=0; _fecdn_=1; __uuid=1530526874197.29; _mscid=s_00_000; _uuid=5A82BEABFFA844194AC27B0A9571E0FD; slide_guide_home=1; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1530526875,1530526887,1530527132; ADHOC_MEMBERSHIP_CLIENT_ID1.0=023d7239-8a70-503b-b065-89ab0cb831b1; firsIn=1; __tlog=1530526874199.05%7C00000000%7CR000000075%7Cs_00_000%7Cs_00_000; JSESSIONID=22D674C03C6271411323C1186E82AB6D; __session_seq=18; __uv_seq=18; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1530542542",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",

        }

    }

    def parse(self,response):
        url = 'https://www.liepin.com/zhaopin/?ckid=d80fb75b21a31141&fromSearchBtn=2&degradeFlag=0&init=-1&headckid=d80fb75b21a31141&d_pageSize=40&siTag=1B2M2Y8AsgTpgAmY7PhCfg~fA9rXquZc5IkJpXC-Ycixw&d_headId=9e4036f8fc251a85383c191b1f843367&d_ckId=9e4036f8fc251a85383c191b1f843367&d_sfrom=search_unknown&d_curPage=0&curPage=%d'
        for i in range(99,0,-1):
            base_url = url % i
            yield scrapy.Request(base_url,callback=self.get_info)

    def get_info(self,response):
        # print('分页'*50)
        # print(response.url)
        detail_url_list = response.css('div.job-info h3 a::attr(href)').extract()
        for detail_url in detail_url_list:

            yield scrapy.Request(detail_url,callback=self.get_detail)
            # time.sleep(0.1)
    def get_detail(self,response):
        # print('详情'*50)
        # print(response.url)
        # time.sleep(0.5)
        item = JobsItem()
        job_url = response.url
        job_name = response.css('div.title-info h1::text').extract_first()
        money = response.css('p.job-item-title::text').extract()[0].strip('\r\n ')
        job_smoney,job_emoney = self.get_money(money)

        job_location = response.css('p.basic-infor span a::text').extract_first()
        job_putime = response.css('p.basic-infor time::attr(title)').extract_first()
        info = response.css('div.job-qualifications span::text').extract()

        job_educa = info[0]
        suffer = info[1]
        if '经验不限' in suffer:
            job_ssuffer = 0
            job_esuffer = 0
        else:
            job_ssuffer = info[1].strip('年以上')
            job_esuffer = job_ssuffer

        job_tags = ','.join(response.css('div.tag-list span::text').extract())

        job_info = ','.join(response.css('div.job-description div::text').extract())

        job_type = response.xpath('//div[@class="job-item main-message"]/div/ul/li[1]/label/text()').extract_first()
        job_cname = response.xpath('//div[@class="company-logo"]/p/a/text()').extract_first()
        job_address = response.xpath('//ul[@class="new-compintro"]/li[last()]/text()').extract_first().split('：')[-1]

        crawl_time = datetime.datetime.now().strftime('%Y-%m-%d')

        item["job_url"] = job_url
        # 职位名
        item["job_name"] = job_name
        # 所在地
        item["job_location"] = job_location
        # 工资
        item["job_smoney"] = job_smoney
        item["job_emoney"] = job_emoney
        # 公司名
        item["job_cname"] = job_cname
        # 经验
        item["job_ssuffer"] = job_ssuffer
        item["job_esuffer"] = job_esuffer
        # 学历
        item["job_educa"] = job_educa
        # 发布时间
        item["job_putime"] = job_putime
        # 标签
        item["job_tags"] = job_tags
        # 职位详情
        item["job_info"] = job_info
        # 职位类型
        item["job_type"] = job_type
        # 公司地址
        item["job_address"] = job_address

        item['spider'] = "liepin"

        item['crawltime'] = crawl_time

        yield item
        # print(job_type,job_cname,job_address)

    def get_money(self,value):
        res = value.split('-')
        if '面议' in value:
            smoney = 0
            emoney = 0
        elif '-' in value:
            smoney = round(int(res[0]) / 12 * 10)
            emoney = round(int(res[1].strip('万')) / 12 * 10)
        else:
            smoney = 0
            emoney = 0
        return smoney,emoney
