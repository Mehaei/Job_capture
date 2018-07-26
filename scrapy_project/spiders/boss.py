import scrapy

class BossSpider(scrapy.Spider):
    name = "boss"
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/gongsir/fa2f92669c66eee31Hc~.html?']

    def parse(self, response):

        url = "https://www.zhipin.com/gongsir/fa2f92669c66eee31Hc~.html?page=%d"

        for i in range(30,0,-1):
            base_url = url % i
            yield scrapy.Request(base_url,callback=self.get_detail)

    def get_detail(self,response):
        print(response.text)
