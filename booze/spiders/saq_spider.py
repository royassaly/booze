import scrapy
import unicodedata

from booze.items import BoozeItem

class SaqSpider(scrapy.Spider):
    name = "saq"
    allowed_domains = ["saq.com"]
    start_urls = [
    # FOR TESTING:
    #  "http://www.saq.com/webapp/wcs/stores/servlet/SearchDisplay?searchType=&orderBy=1&categoryIdentifier=050806&showOnly=product&langId=-1&beginIndex=0&tri=&pageSize=100&pageView=List&catalogId=50000&sensTri=&facet=&storeId=20002"
    #  There are 6 pages of results for Scotch and Whisky. Get them all! beginIndex is your friend.
       "http://www.saq.com/webapp/wcs/stores/servlet/SearchDisplay?searchType=&orderBy=&categoryIdentifier=0508&showOnly=product&langId=-1&beginIndex=0&tri=&pageSize=100&pageView=&catalogId=50000&sensTri=&facet=&storeId=20002",
       "http://www.saq.com/webapp/wcs/stores/servlet/SearchDisplay?searchType=&orderBy=&categoryIdentifier=0508&showOnly=product&langId=-1&beginIndex=100&tri=&pageSize=100&pageView=&catalogId=50000&sensTri=&facet=&storeId=20002",
       "http://www.saq.com/webapp/wcs/stores/servlet/SearchDisplay?searchType=&orderBy=&categoryIdentifier=0508&showOnly=product&langId=-1&beginIndex=200&tri=&pageSize=100&pageView=&catalogId=50000&sensTri=&facet=&storeId=20002",
       "http://www.saq.com/webapp/wcs/stores/servlet/SearchDisplay?searchType=&orderBy=&categoryIdentifier=0508&showOnly=product&langId=-1&beginIndex=300&tri=&pageSize=100&pageView=&catalogId=50000&sensTri=&facet=&storeId=20002",
       "http://www.saq.com/webapp/wcs/stores/servlet/SearchDisplay?searchType=&orderBy=&categoryIdentifier=0508&showOnly=product&langId=-1&beginIndex=400&tri=&pageSize=100&pageView=&catalogId=50000&sensTri=&facet=&storeId=20002",
       "http://www.saq.com/webapp/wcs/stores/servlet/SearchDisplay?searchType=&orderBy=&categoryIdentifier=0508&showOnly=product&langId=-1&beginIndex=500&tri=&pageSize=100&pageView=&catalogId=50000&sensTri=&facet=&storeId=20002"
    ]
    
    custom_settings = {
    # specifies exported fields and order
    'FEED_EXPORT_FIELDS': ["title", "alcohol", "volume", "sale", "savings", "price", "inventory", "link"],
    }

    def parse(self, response):
        for href in response.xpath("//div[@id='resultatRecherche']/div/div/div[@class='wapProduit']/p/a/@href"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        for sel in response.xpath("//div[@class='product-bloc-fiche']"):
            item = BoozeItem()
            price = 0
            item['sale'] = ''
            item['savings'] = ''
            item['alcohol'] = ''
            # Deal with SAQ inventory - TODO
            item['inventory'] = ''
            
            item['title'] = response.xpath("//h1/text()").extract()
            item['link'] = response.url
            # Regular price
            price = response.xpath("//p[@class='price']/text()").extract()  
             # Sale price          
            if len(price) == 0:
              item['sale'] = "On sale!"
              price =  response.xpath("//p[@class='price price-rebate']/text()").extract()[0].strip()
              item['savings'] = response.xpath("//p[@class='discount']/span/following-sibling::text()").extract()[0].strip()
            item['price'] = price
            volume = []
            # Use the details information <div>
            # response.xpath("//div[@class='left']/child::span[text()='Size']/parent::div/../div/text()").extract()[0].strip()
            # Note the word "Size", as we can reuse this for region, alcohol, etc.
            volume = response.xpath("//div[@class='left']/child::span[text()='Size']/parent::div/../div/text()").extract()[0].strip()
            # returns the u'750\xa0ml' which has some garbage data in it which needs to be removed below
            item['volume'] = unicodedata.normalize("NFKD", volume)
            
            # Get the alcohol % from the details info area:
            alcohol = []
            alcohol = response.xpath("//div/child::span[text()='Degree of alcohol']/parent::div/../div/text()").extract()[0].strip()
            item['alcohol'] = unicodedata.normalize("NFKD", alcohol)
            
            yield item