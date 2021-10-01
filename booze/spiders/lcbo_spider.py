import scrapy
import unicodedata

from booze.items import BoozeItem

class LcboSpider(scrapy.Spider):
    name = "lcbo"
    allowed_domains = ["lcbo.com"]
    start_urls = [
      # URLs to scrape
     "https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/spirits-15/spirits-15/whisky-whiskey-15020?pageView=grid&orderBy=1&fromPage=catalogEntryList&pageSize=100&beginIndex=0",
     "https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/spirits-15/spirits-15/whisky-whiskey-15020?pageView=grid&orderBy=1&fromPage=catalogEntryList&pageSize=100&beginIndex=100",
     "https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/spirits-15/spirits-15/whisky-whiskey-15020?pageView=grid&orderBy=1&fromPage=catalogEntryList&pageSize=100&beginIndex=200",
     "https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/spirits-15/spirits-15/whisky-whiskey-15020?pageView=grid&orderBy=1&fromPage=catalogEntryList&pageSize=100&beginIndex=300",
     "https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/spirits-15/spirits-15/whisky-whiskey-15020?pageView=grid&orderBy=1&fromPage=catalogEntryList&pageSize=100&beginIndex=400",
     "https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/spirits-15/spirits-15/whisky-whiskey-15020?pageView=grid&orderBy=1&fromPage=catalogEntryList&pageSize=100&beginIndex=500",
     "https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/spirits-15/spirits-15/whisky-whiskey-15020?pageView=grid&orderBy=1&fromPage=catalogEntryList&pageSize=100&beginIndex=600",
     "https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/spirits-15/spirits-15/whisky-whiskey-15020?pageView=grid&orderBy=1&fromPage=catalogEntryList&pageSize=100&beginIndex=700",
     "https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/spirits-15/spirits-15/whisky-whiskey-15020?pageView=grid&orderBy=1&fromPage=catalogEntryList&pageSize=100&beginIndex=800"
 ]
  
    custom_settings = {
    # specifies exported fields and order
    'FEED_EXPORT_FIELDS': ["title", "alcohol", "volume", "sale", "savings", "price", "inventory", "link"],
    }

    def parse(self, response):
        for href in response.xpath("//div[@class='productChart']/div[@class='product_name']/a/@href"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = BoozeItem()
        volume = []
        rangeVolumeBottle = len(" bottle")
        rangePriceSavings = len("Save :")
        item['title'] = ''
        item['sale'] = ''
        item['savings'] = ''
        item['alcohol'] = ''
        item['inventory'] = ''
        # old_price = 0
        savings = 0
        #checkInventoryURL = ''
        #inventoryPage = []
        
        item['title'] = response.xpath("//div/h1[@role='heading']/text()").extract()[0].strip()
        item['link'] = response.url
        # OLD: item['price'] = response.xpath("//span[@class='price']/text()").extract()[0].strip()

        item['price'] = response.xpath("//div[@class='top namePartPriceContainer']/div/span[@class='price']/text()").extract()[0].strip()

        # old_price = response.xpath("//span[@class='listPrice_old']/text()").extract()
        # OLD savings = response.xpath("//span[@class='listPrice_save']/text()").extract()

        savings = response.xpath("//div[@class='top namePartPriceContainer']/div/div[@class='listPrice']/span[@class='listPrice_save']/text()")
                  
                  
        if len(savings) > 0:
            item['sale'] = "On sale!"
            savings = response.xpath("//div[@class='top namePartPriceContainer']/div/div[@class='listPrice']/span[@class='listPrice_save']/text()").extract()[0].strip()
            item['savings'] = savings[rangePriceSavings:]
           
       
        volume = response.xpath("//dl[@class='product-details-list']/dd/b/text()").extract()[0].strip()
        item['volume'] = volume[0:len(volume)-rangeVolumeBottle]
          
        # Get the alcohol % from the product details section 
        # OLD:  alcohol = response.xpath("//div[@class='product-details-list']/div/b[text() = 'Alcohol/Vol:']/following-sibling::span[1]/text()").extract()[0].strip()
        alcohol = response.xpath("//dl[@class='product-details-list']/dd/span/text()").extract()[0].strip()
        item['alcohol'] = alcohol

        # Rewrite all of the code below. HTML has changed again on the LCBO website.

        # Check if the item if even available, if not: Sorry, the product you selected is currently not available in any store.
        #checkInventoryURL = response.xpath("//button[@id='check-store-inventory']/@data-modal-content").extract()[0].strip()
        #request =  scrapy.Request(str(checkInventoryURL),callback=self.inventory_parse)
        #request.meta['item'] = item     
        #yield request
           
  #  def inventory_parse(self,response):
   #     item = BoozeItem()
   #     item = response.meta['item']
  #      item['inventory'] = '' # response.xpath("//td[@class='no-inventory']/text()").extract()
        yield item