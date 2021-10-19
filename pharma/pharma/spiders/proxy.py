import scrapy


class ProxySpider(scrapy.Spider):
    
    name = 'proxy'
    allowed_domains = ['free-proxy-list.net']
    start_urls = ['https://free-proxy-list.net/']
    
    def parse(self, response):
        ip_column = response.xpath('//section[@id="list"]//div[@class="table-responsive"]//tbody//tr/td[1]/text()').getall()
        port_column = response.xpath('//section[@id="list"]//div[@class="table-responsive"]//tbody//tr/td[2]/text()').getall()
        proxies_list = []
        for i in range(len(ip_column)):
            proxy = ip_column[i]+':'+port_column[i]
            proxies_list.append(proxy)
            
        with open("proxies.txt", "w") as file:
            for proxy in proxies_list:
                file.write(proxy+"\n")
            