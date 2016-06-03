import scrapy

from booze.items import BoozeItem

class LcboSpider(scrapy.Spider):
    name = "lcbo"
    allowed_domains = ["lcbo.com"]
    start_urls = [
      'http://www.lcbo.com/lcbo/catalog/scotch-single-malts/11086?contentBeginIndex=0&productBeginIndex=%d&beginIndex=%d&orderBy=&categoryPath=spirits/whisky-whiskey/scotch-single-malts&orderByContent=&facet=&storeId=10151&catalogId=10001&langId=-1&requesttype=ajax' %(n*12, n*12) for n in range(0, 11)
    ]

    def parse(self, response):
        for sel in response.xpath("//div[@class='row products list-view']/div"):
            item = BoozeItem()
            # response.xpath("//div[@class='row products list-view']/div/div/a/@title").extract()
            item['title'] = sel.xpath("div[@class='product-name']/a/@title").extract()
            item['link'] = 'http://www.lcbo.com' + str(sel.xpath("div[@class='product-name']/a/@href").extract()[0].strip())
            # response.xpath("//div[@class='row products list-view']/div/div/div/div[@class='price']/text()").extract()
            item['price'] = sel.xpath("div/div/div[@class='price']/text()").extract()
            yield item