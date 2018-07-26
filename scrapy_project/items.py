# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobsItem(scrapy.Item):
    job_url = scrapy.Field()
    # 职位名
    job_name = scrapy.Field()
    # 所在地
    job_location = scrapy.Field()
    # 工资
    job_smoney = scrapy.Field()
    job_emoney = scrapy.Field()
    # 公司名
    job_cname = scrapy.Field()
    # 经验
    job_ssuffer = scrapy.Field()
    job_esuffer = scrapy.Field()
    # 学历
    job_educa = scrapy.Field()
    # 发布时间
    job_putime = scrapy.Field()
    # 标签
    job_tags = scrapy.Field()
    # 职位详情
    job_info = scrapy.Field()
    # 职位类型
    job_type = scrapy.Field()
    # 公司地址
    job_address = scrapy.Field()

    spider = scrapy.Field()

    crawltime = scrapy.Field()

    def get_sql(self):
        sql = "insert into jobs(job_url,job_name,job_location,job_smoney,job_emoney,job_cname,job_ssuffer,job_esuffer,job_educa,job_putime,job_tags,job_info,job_type,job_address,spider,crawltime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        data = (self['job_url'],self['job_name'],self['job_location'],self['job_smoney'],self['job_emoney'],self['job_cname'],self['job_ssuffer'],self['job_esuffer'],self['job_educa'],self['job_putime'],self['job_tags'],self['job_info'],self['job_type'],self['job_address'],self['spider'],self['crawltime'])

        return sql,data

