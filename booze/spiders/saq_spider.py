import scrapy

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
            yield item
            
   
''' WORKING FROM MAIN PAGE LIST
    def parse(self, response):
        for sel in response.xpath("//div[@id='resultatRecherche']"):
            item = BoozeItem()
            item['title'] = sel.xpath("div/div/div[@class='wapProduit']/p/a/text()").extract()
            item['link'] = sel.xpath("div/div/div[@class='wapProduit']/p/a/@href").extract()
            item['price'] = sel.xpath("//td[@class='price']/a/text()").extract()
            yield item
'''