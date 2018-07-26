# -*- coding: utf-8 -*-
import scrapy
import hashlib
import datetime
from scrapy_project.items import JobsItem
import json
from urllib import request
import re
from scrapy_project.items import JobsItem
class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = []
    start_urls = ['https://sou.zhaopin.com/?jl=530&jt=']

    get_num = re.compile(r'\d+')
    custom_settings = {
        "CONCURRENT_REQUESTS": 32,
        "ITEM_PIPELINES": {
            'scrapy_project.pipelines.MysqlPipeline': 1,
        },
    }



    def parse(self, response):
        url_list = ['https://xiaoyuan.zhaopin.com/full/0/0_0_0_0_0_-1_0_1_0','https://sou.zhaopin.com/?jl=530&jt=','http://www.highpin.cn/zhiwei/all.html']
        for url in url_list:
            if 'xiaoyuan' in url:
                pass
                # yield scrapy.Request(url,callback=self.get_xiaoyuan_info)
            elif 'sou' in url:
                # pass
                yield scrapy.Request(url,callback=self.get_sou_info)
            else:
                # pass
                yield scrapy.Request(url,callback=self.get_zhuopin_info)

# ----------------------------------------------------------卓聘职位--------------------------------------------------------------------------


    def get_zhuopin_info(self,response):
        url = "http://www.highpin.cn/zhiwei/p_%d.html"
        for i in range(150,0,-1):
            base_url = url % i
            yield scrapy.Request(base_url,callback=self.get_detail_list)

    def get_detail_list(self,response):
        detail_list = response.xpath('//div[@class="jobInfoItem clearfix bor-bottom add-bg"]//a/@href').extract()
        for url in detail_list:
            detail_url = request.urljoin(response.url,url)
            yield scrapy.Request(detail_url,callback=self.get_zhuopin_detail)

    def get_zhuopin_detail(self,response):
        item = JobsItem()
        job_url = response.url
        job_name = response.css('.cursor-d ::attr(title)').extract_first()
        tags = response.css('.labelList.lh14.mar-B4  span::text').extract()
        if tags:
            job_tags = ','.join(tags)
        else:
            job_tags = '无标签'

        job_cname = response.xpath('//div[@class="mainContent"]/div[1]/ul/li/a/text()').extract_first()
        job_address = response.xpath('//div[@class="mainContent"]/div[1]/ul/li/span/@title').extract()[-1]

        job_putime = response.xpath('//ul[@class="view-ul view-wid344"]/li/span/text()').extract()[-1]

        info1 = response.xpath('//ul[@class="view-ul view-wid344"]/li/@title').extract()
        job_type = info1[0]
        job_location = info1[-1]

        money = response.xpath('//li[@class="mar-b8"]/span/a/text()').extract()[0]
        '''
        10-100万 1 年及以上
        11-16万 不限
        '''

        job_smoney = round(float(money.split('-')[0]) / 12 * 10)
        job_emoney = round(float(money.split('-')[-1].strip('万')) / 12 * 10)

        suffer = response.xpath('//ul[@class="view-ul view-wid230 clearfix"]/li/span/text()').extract()[0]

        if '以上' in suffer:
            res = self.get_num.search(suffer)
            job_ssuffer = res.group()
            job_esuffer = res.group()
        else:
            job_ssuffer = 0
            job_esuffer = 0

        info = response.xpath('//div[@class="mar-b8 clearfix"]/div/p/text()').extract()
        job_info = str(info)
        job_educa = response.xpath('//ul[@class="view-ul view-wid230 clearfix"]/li/text()').extract()[-1].strip()

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

        item['spider'] = "zhilian"

        item['crawltime'] = crawl_time

        yield item

        # print(money,job_smoney,job_emoney,suffer,job_ssuffer,job_esuffer)

# ----------------------------------------------------------卓聘职位结束--------------------------------------------------------------------------



#----------------------------------------------------------首页搜索职位--------------------------------------------------------------------------
    def get_sou_info(self,response):
        #:第一页
        # url = "https://fe-api.zhaopin.com/c/i/sou?pageSize=60&cityId=530&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kt=3"
        # 二
        url = "https://fe-api.zhaopin.com/c/i/sou?start=%d&pageSize=60&cityId=530&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kt=3"
        for i in range(30,0,-1):
            if i == 1:
                base_url = "https://fe-api.zhaopin.com/c/i/sou?pageSize=60&cityId=530&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kt=3"
            else:
                page = (i-1)*60
                base_url = url% page

            yield scrapy.Request(base_url,callback=self.get_sou_detail_list)
        # print('get_spu_info',response.url)

    def get_sou_detail_list(self,response):
        data_list = json.loads(response.text)
        for data in data_list['data']['results']:
            item = JobsItem()
            job_url = data['positionURL']
            job_name = data['jobName']
            job_type = data['jobType']['display']
            job_cname = data['company']['name']

            suffer = data['workingExp']['name']
            job_ssuffer,job_esuffer = self.get_suffer(suffer)

            money = data['salary']
            job_smoney,job_emoney = self.get_money(money)

            job_educa = data['eduLevel']['name']
            job_location = data['city']['items'][0]['name']
            job_putime = data['createDate'].split()[0]
            tags = data['welfare']
            if tags:
                job_tags = ','.join(tags)
            else:
                job_tags = "无标签"

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

            # 职位类型
            item["job_type"] = job_type


            item['spider'] = "zhilian"

            item['crawltime'] = crawl_time

            yield scrapy.Request(job_url,callback=self.get_sou_detail,meta={"item":item})
            # print(suffer,job_ssuffer,job_esuffer,money)

    def get_sou_detail(self,response):
        item = response.meta['item']
        job_address = response.xpath('//div[@class="tab-inner-cont"]/h2/text()').extract()[0]
        job_info = ','.join(response.xpath('//div[@class="tab-inner-cont"]/p/text()').extract())
        # 公司地址
        item["job_address"] = job_address
        # 职位详情
        item["job_info"] = job_info
        yield item

        # print(job_address,job_info)

# ----------------------------------------------------------首页搜索职位结束--------------------------------------------------------------------------

    # 邮箱正则 /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/

# --------------------------------------校园招聘--------------------------------------------------------------------------
    def get_xiaoyuan_info(self,response):
        url = "https://xiaoyuan.zhaopin.com/full/0/0_0_0_0_0_-1_0_%d_0"
        for i in range(500,0,-1):
            base_url = url % i
            yield scrapy.Request(base_url,callback=self.get_xiaoyuan_detail_list)
        # print('get_xiaoyuan_info',response.url)

    def get_xiaoyuan_detail_list(self,response):
        detail_url_list = response.xpath('//p[@class="searchResultJobName"]/a/@href').extract()
        for url in detail_url_list:
            detail_url = 'https:' + url
            yield scrapy.Request(detail_url,callback=self.get_xiaoyuan_detail)

    def get_xiaoyuan_detail(self,response):
        item = JobsItem()
        url = response.url
        md5 = hashlib.md5()
        md5.update(url.encode(encoding="utf-8"))

        job_url = md5.hexdigest()
        job_name = response.css('#JobName::text').extract()[0].strip()
        job_cname = response.css('#jobCompany a::text').extract_first()

        job_type= response.css('.cJobDetailInforWd2.marb::text').extract()
        if len(job_type) >= 1:
            job_type = job_type[0].strip()
        else:
            job_type = "未知"
        job_location = response.css('#currentJobCity::attr(title)').extract()[0]
        job_putime = response.css('#liJobPublishDate::text').extract()[0]
        job_info = ','.join(response.css('.cJob_Detail.f14 p::text').extract()[1:])
        job_address = response.css('.clearfix.p20 p::text').extract()[0].strip()

        crawl_time = datetime.datetime.now().strftime('%Y-%m-%d')

        item["job_url"] = job_url
        # 职位名
        item["job_name"] = job_name
        # 所在地
        item["job_location"] = job_location
        # 工资
        item["job_smoney"] = 0
        item["job_emoney"] = 0
        # 公司名
        item["job_cname"] = job_cname
        # 经验
        item["job_ssuffer"] = 0
        item["job_esuffer"] = 0
        # 学历
        item["job_educa"] = "应届生"
        # 发布时间
        item["job_putime"] = job_putime
        # 标签
        item["job_tags"] = "工作轻松"
        # 职位详情
        item["job_info"] = job_info
        # 职位类型
        item["job_type"] = job_type
        # 公司地址
        item["job_address"] = job_address

        item['spider'] = "zhilianxiaoyuan"

        item['crawltime'] = crawl_time

        yield item

# --------------------------------------校园招聘结束--------------------------------------------------------------------------


    # def get_zhuopin_info(self,response):
    #     print('get_zhuopin_info',response.url)


# ------------------------------------------------提取工资和经验---------------------------------------------------------------------

    # 首页搜索的钱和经验类型
    '''
    不限 4K-6K
    1-3年 10K-20K
    无经验 4K-6K
    1年以下 8K-10K
    '''


    def get_money(self,value):
        if '-' in value:
            res = self.get_num.findall(value)
            smoney = res[0]
            emoney = res[1]
        else:
            smoney = 0
            emoney = 0

        return smoney,emoney

    def get_suffer(self,value):

        if '以下' in value:
            res = self.get_num.search(value)
            ssuffer = res.group()
            esuffer = res.group()
        elif '-' in value:
            res = self.get_num.findall(value)
            ssuffer = res[0]
            esuffer = res[1]
        elif '以上' in value:
            res = self.get_num.search(value)
            ssuffer = res.group()
            esuffer = res.group()
        else:
            ssuffer = 0
            esuffer = 0
        return ssuffer,esuffer