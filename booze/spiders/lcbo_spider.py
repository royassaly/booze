import scrapy
import unicodedata

from booze.items import BoozeItem

class LcboSpider(scrapy.Spider):
    name = "lcbo"
    allowed_domains = ["lcbo.com"]
    # Scotch, Scotch Whisky Blend = [11086, 11083], All Scotch and Whisky = [11014]
    categories = [11014]
    # Set max value to 60 since there are 60 pages
    start_urls = [
      # FOR TESTING:
      #'http://www.lcbo.com/lcbo/catalog/scotch-single-malts/{}?contentBeginIndex=0&productBeginIndex=%s&beginIndex=%s&orderBy=&categoryPath=spirits/whisky-whiskey/scotch-single-malts&orderByContent=&facet=&storeId=10151&catalogId=10001&langId=-1&requesttype=ajax'.format(c) %(n*12, n*12) for n in range(0, 12) for c in categories
      'http://www.lcbo.com/lcbo/catalog/scotch-single-malts/{}?contentBeginIndex=0&productBeginIndex=%s&beginIndex=%s&orderBy=&categoryPath=spirits/whisky-whiskey/scotch-single-malts&orderByContent=&facet=&storeId=10151&catalogId=10001&langId=-1&requesttype=ajax'.format(c) %(n*12, n*12) for n in range(0, 60) for c in categories
    ]
    
    custom_settings = {
    # specifies exported fields and order
    'FEED_EXPORT_FIELDS': ["title", "alcohol", "volume", "sale", "savings", "price", "inventory", "link"],
    }

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
        item['alcohol'] = ''
        item['inventory'] = ''
        savings = 0
        checkInventoryURL = ''
        inventoryPage = []
        
        item['title'] = response.xpath("//div/h1/text()").extract()[0].strip()
        item['link'] = response.url
        item['price'] = response.xpath("//span[@class='price-value']/text()").extract()[0].strip()
        savings = response.xpath("//small[@class='saving']/text()").extract()
        if len(savings) == 2:
            item['sale'] = "On sale!"
            item['savings'] = savings[1]
        volume = response.xpath("//dt[@class='product-volume']/text()").extract()
        item['volume'] = volume
        
        # u'750 mL'
        # Sometimes the LCBO puts "750 mL gift" instead of "750 ml bottle". Weird. FIX ME!
        if "gift" in volume[0]:
          item['volume'] = [elem[:len(elem) - rangeVolumeGift] for elem in volume]
          
        # Get the alcohol % from the product details section 
        alcohol = response.xpath("//dt[text() = 'Alcohol/Vol']/following-sibling::dd[1]/text()").extract()
        item['alcohol'] = alcohol
        
        # Check if the item if even available, if not: Sorry, the product you selected is currently not available in any store.
        checkInventoryURL = response.xpath("//button[@id='check-store-inventory']/@data-modal-content").extract()[0].strip()
        request =  scrapy.Request(str(checkInventoryURL),callback=self.inventory_parse)
        request.meta['item'] = item     
        yield request
           
    def inventory_parse(self,response):
        item = BoozeItem()
        item = response.meta['item']
        item['inventory'] = response.xpath("//td[@class='no-inventory']/text()").extract()
        yield item
        
