import scrapy
from ebooks_scrap.items import EbooksScrapItem
from scrapy.loader import ItemLoader
import time

class ebookSpider(scrapy.Spider):
    name = "ebook"
    start_urls = [ "https://books.toscrape.com/", "https://books.toscrape.com/catalogue/" ]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.page_count = 0

    def parse(self, response):
        self.page_count += 1
        # getting all the article elements
        ebooks = response.css("article.product_pod")

        for ebook in ebooks:
            # extracting the details page url
            url = ebook.css("h3 a").attrib["href"]
            # sending a request to the details page
            if self.page_count == 1:
                yield scrapy.Request(
                    url = self.start_urls[0] + url,
                    callback = self.parse_details
                )
            else:
                yield scrapy.Request(
                    url = self.start_urls[1] + url,
                    # Callback to the previous url
                    callback = self.parse_details
                )

        print(["PAGE COUNT : ", self.page_count])
        time.sleep(2)

        # For next page
        next_btn = response.css("li.next a")
        if next_btn:
            if next_btn.attrib["href"] == "catalogue/page-2.html":
                next_value = self.start_urls[0] + next_btn.attrib["href"]
                yield scrapy.Request(url=next_value)
            # elif next_btn.attrib["href"] == "page-3.html":
            #     exit()
            else:
                next_value = self.start_urls[1] + next_btn.attrib["href"]
                yield scrapy.Request(url=next_value)


    # For entering the url and fetching the data
    def parse_details(self, response):
        main = response.css("div.product_main")
        loader = ItemLoader(item=EbooksScrapItem(), selector=main)
        loader.add_css("title", "h1::text")
        loader.add_css("price", "p.price_color::text")
        quantity_p = main.css("p.availability")
        loader.add_value(
            "in_stock", 
            quantity_p.re(r'\(.+ available\)')[0]
            # Regular Expressions used:
            # \ - escape character or treat 
            #     as normal character.
            # . - any character (a-Z, 0-9, $, %, etc.)
            # + - one or more characters
        )

        # Extracting from Table
        table = response.css("table.table-striped")
        product_details = {}
        for rows in table.css("tr"):
            heading = rows.css("th::text").get()
            data = rows.css("td::text").get()
            product_details[heading]=data
            loader.add_value("product_information", product_details)
        
        yield loader.load_item()
