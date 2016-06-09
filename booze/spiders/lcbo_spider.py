import scrapy
import unicodedata

from booze.items import BoozeItem

class LcboSpider(scrapy.Spider):
    name = "lcbo"
    allowed_domains = ["lcbo.com"]
    # Scotch, Scotch Whisky Blend
    categories = [11086, 11083]
    start_urls = [
      'http://www.lcbo.com/lcbo/catalog/scotch-single-malts/{}?contentBeginIndex=0&productBeginIndex=%s&beginIndex=%s&orderBy=&categoryPath=spirits/whisky-whiskey/scotch-single-malts&orderByContent=&facet=&storeId=10151&catalogId=10001&langId=-1&requesttype=ajax'.format(c) %(n*12, n*12) for n in range(0, 12) for c in categories
    ]

    def parse(self, response):
        for href in response.xpath("//div[@class='row products list-view']/div/div[@class='product-name']/a/@href"):
            url = 'http://www.lcbo.com' + href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = BoozeItem()
        volume = []
        price = 0
        rangeVolume = len(" bottle")
        rangePrice = len(" ")
        item['sale'] = ''
        item['savings'] = ''
        savings = 0
        
        item['title'] = response.xpath("//div/h1/text()").extract()[0].strip()
        item['link'] = response.url
        price = response.xpath("//div/strong/text()").extract()
        if len(price) == 2:
          if 'Limited Time Offer' in price[1]:
            item['sale'] = "On sale!"
            savings = response.xpath("//span[@class='saving']/text()").extract()[0]
            item['savings'] = savings[5:]  
        item['price'] = response.xpath("//div/strong/text()").extract()[0]
        volume = response.xpath("//dt[@class='product-volume']/text()").extract()
        
        # u'750 mL bottle', u'750 mL bottle',
        # truncate the text " bottle" at tend of each string in the array
        # Sometimes the LCBO puts "750 mL gift" instead of "750 ml bottle". Weird. Fix it later.
        item['volume'] = [elem[:len(elem) - rangeVolume] for elem in volume]          
        yield item