import scrapy
import unicodedata

from booze.items import BoozeItem

class SaqSpider(scrapy.Spider):
    name = "saq"
    allowed_domains = ["saq.com"]
    start_urls = [
    # FOR TESTING
    #  "http://www.saq.com/webapp/wcs/stores/servlet/SearchDisplay?searchType=&orderBy=1&categoryIdentifier=050806&showOnly=product&langId=-1&beginIndex=0&tri=&pageSize=100&pageView=List&catalogId=50000&sensTri=&facet=&storeId=20002"
       "http://www.saq.com/webapp/wcs/stores/servlet/SearchDisplay?searchType=&orderBy=1&categoryIdentifier=050806&showOnly=product&langId=-1&beginIndex=0&tri=&pageSize=100&pageView=List&catalogId=50000&sensTri=&facet=&storeId=20002",
        # 100 to 200 List of booze
       "http://www.saq.com/webapp/wcs/stores/servlet/SearchDisplay?searchType=&orderBy=1&categoryIdentifier=050806&showOnly=product&langId=-1&beginIndex=100&tri=&pageSize=100&pageView=List&catalogId=50000&sensTri=&facet=&storeId=20002",
        # 200+ List of booze
        "http://www.saq.com/webapp/wcs/stores/servlet/SearchDisplay?searchType=&orderBy=1&categoryIdentifier=050806&showOnly=product&langId=-1&beginIndex=200&tri=&pageSize=100&pageView=List&catalogId=50000&sensTri=&facet=&storeId=20002"
  ]

    def parse(self, response):
        for href in response.xpath("//div[@id='resultatRecherche']/div/div/div[@class='wapProduit']/p/a/@href"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        for sel in response.xpath("//div[@class='product-bloc-fiche']"):
            item = BoozeItem()
            item['title'] = sel.xpath("//h1/text()").extract()
            item['link'] = response.url
            item['price'] = sel.xpath("//p[@class='price']/text()").extract()
            volume = []
            # Use the details information <div>
            # response.xpath("//div[@class='left']/child::span[text()='Size']/parent::div/../div/text()").extract()[0].strip()
            # Note the word "Size", as we can reuse this for region, alcohol, etc.
            volume = sel.xpath("//div[@class='left']/child::span[text()='Size']/parent::div/../div/text()").extract()[0].strip()
            # returns the u'750\xa0ml' which has some garbage data in it which needs to be removed below
            item['volume'] = unicodedata.normalize("NFKD", volume)            
            yield item