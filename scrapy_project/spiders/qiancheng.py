import scrapy
import re
from scrapy_project.items import JobsItem
import datetime
class QianChengSpider(scrapy.Spider):
    name = 'qiancheng'
    allowed_domains = []
    start_urls = ['https://search.51job.com/jobsearch/search_result.php']

    custom_settings = {
        "CONCURRENT_REQUESTS": 32,
        "ITEM_PIPELINES" : {
           'scrapy_project.pipelines.MysqlPipeline': 1,
        }

    }
    get_num = re.compile(r'\d+')
    def parse(self, response):
        url = "https://search.51job.com/list/000000,000000,0000,00,2,99,2B,2,%d.html"
        for i in range(100,0,-1):
            base_url = url % i
            yield scrapy.Request(base_url,callback=self.get_info)

    def get_info(self,response):

        detail_url_list = response.css('div#resultList div.el p.t1 span a::attr(href)').extract()
        # print(detail_url_list)
        for detail_url in detail_url_list:
            yield scrapy.Request(detail_url,callback=self.get_detail)

    def get_detail(self,response):
        item = JobsItem()
        # https://jobs.51job.com/jinan/55649861.html?s=01&t=0 ['SEO专员'] ['济南'] ['3-6千/月'] ['山东欣希安药业股份有限公司'] ['\r\n\t\t\t\t民营公司    \t\t    \t\t\t\xa0\xa0|\xa0\xa050-150人    \t\t    \t\t    \t\t\t\xa0\xa0|\xa0\xa0制药/生物工程    \t\t\t\t\t']

        job_url = response.url
        # 职位名
        job_name = response.css('div.cn h1::attr(title)').extract_first()
        # 所在地
        job_location = response.css('span.lname::text').extract_first()
        # 工资
        money = response.css('div.cn strong::text').extract_first()
        job_smoney,job_emoney = self.get_money(money)

        # print(money,job_smoney,job_emoney)



        # 公司名
        job_cname = response.css('p.cname a::attr(title)').extract_first()

        # 经验
        info = response.css('div.t1 span::text').extract()

        job_ssuffer,job_esuffer = self.get_suffer(info[0])



        if len(info) <= 3:
            # 学历
            job_educa = "无学历要求"
            # 发布时间
            job_putime = '2018-'+info[-1].strip('发布')
        else:
            job_educa = info[1]
            job_putime = info[3].strip('发布')
        # 标签
        tags = response.css('p.t2 span::text').extract()
        job_tags = ','.join(tags)

        # 职位详情
        info = response.css('div.bmsg.job_msg.inbox p::text').extract()
        job_info = ','.join(info)

        # 职位类型
        job_type = response.css('div.mt10 p span.el::text').extract()[0]

        # 公司地址
        job_address = response.css('div.bmsg.inbox p.fp::text').extract()[-1]
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

        item['spider'] = "qiancheng"

        item['crawltime'] = crawl_time
        yield item

    def get_money(self,value):
        # res = self.get_num.findall(value)
        aa = value.split('-')
        res1 = aa[0]
        res2 = aa[1]
        if '万/月' in res2:
            job_smoney = round(float(res1) * 10)
            job_emoney = round(float(res2.strip('万/月')) * 10)
        elif '万/年' in value:
            job_smoney = round(float(res1) / 12 * 10)
            job_emoney = round(float(res2.strip('万/年')) / 12 * 10)
        else:
            job_smoney = res1
            job_emoney = res2.strip('千/月')
        return job_smoney,job_emoney
    def get_suffer(self,value):
        suffer = self.get_num.findall(value)
        if '-' in value:
            ssuffer = suffer[0]
            esuffer = suffer[1]
        elif len(suffer) == 1:
            ssuffer = suffer[0]
            esuffer = suffer[0]
        else:
            ssuffer = 0
            esuffer = 0

        return ssuffer,esuffer
