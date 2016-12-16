import scrapy
import unicodedata

from booze.items import BoozeItem

class LcboSpider(scrapy.Spider):
    name = "lcbo"
    allowed_domains = ["lcbo.com"]
    # Scotch, Scotch Whisky Blend = [11086, 11083], All Scotch and Whisky = [11014]
    categories = [11014]
    start_urls = [
      # FOR TESTING:
      #'http://www.lcbo.com/lcbo/catalog/scotch-single-malts/{}?contentBeginIndex=0&productBeginIndex=%s&beginIndex=%s&orderBy=&categoryPath=spirits/whisky-whiskey/scotch-single-malts&orderByContent=&facet=&storeId=10151&catalogId=10001&langId=-1&requesttype=ajax'.format(c) %(n*12, n*12) for n in range(0, 12) for c in categories
      'http://www.lcbo.com/lcbo/catalog/scotch-single-malts/{}?contentBeginIndex=0&productBeginIndex=%s&beginIndex=%s&orderBy=&categoryPath=spirits/whisky-whiskey/scotch-single-malts&orderByContent=&facet=&storeId=10151&catalogId=10001&langId=-1&requesttype=ajax'.format(c) %(n*12, n*12) for n in range(0, 52) for c in categories
    ]

    def parse(self, response):
        for href in response.xpath("//div[@class='product-wrapper']/div[@class='product-name']/a/@href"):
            url = 'http://www.lcbo.com' + href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = BoozeItem()
        volume = []
        price = 0
        rangeVolumeBottle = len(" bottle")
        rangeVolumeGift = len(" gift")
        item['sale'] = ''
        item['savings'] = ''
        savings = 0
        
        item['title'] = response.xpath("//div/h1/text()").extract()[0].strip()
        item['link'] = response.url
        item['price'] = response.xpath("//span[@class='price-value']/text()").extract()[0].strip()
        savings = response.xpath("//small[@class='saving']/text()").extract()
        if len(savings) == 2:
            item['sale'] = "On sale!"
            item['savings'] = savings[1]
        volume = response.xpath("//dt[@class='product-volume']/text()").extract()
        
        # u'750 mL bottle'
        # truncate the text " bottle" at tend of each string
        # Sometimes the LCBO puts "750 mL gift" instead of "750 ml bottle". Weird. FIX ME!
        if "gift" in volume[0]:
          item['volume'] = [elem[:len(elem) - rangeVolumeGift] for elem in volume]
        item['volume'] = [elem[:len(elem) - rangeVolumeBottle] for elem in volume]          
        yield item