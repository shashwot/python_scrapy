import scrapy


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    # allowed_domains = ['quotes.toscrape.com']
    # start_urls = ['http://quotes.toscrape.com/']
    
    def start_requests(self):
        yield scrapy.Request(
            "https://quotes.toscrape.com/js",
            meta={
                "playwright": True
            }
        )

    def parse(self, response):
        for quotes in response.css("div.quote span.text::text").getall():
            yield {
                "quotes": quotes
            }
