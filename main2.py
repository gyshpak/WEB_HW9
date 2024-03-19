import scrapy
from scrapy.crawler import CrawlerProcess


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    custom_settings = {"FEED_EXPORT_ENCODING": "utf-8", "FEED_FORMAT": "json", "FEED_URI": "quotes.json"}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").get(),
                "quote": quote.xpath("span[@class='text']/text()").get(),
            } 
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

class AuthorSpider(scrapy.Spider):
    name = "authors"
    custom_settings = {"FEED_EXPORT_ENCODING": "utf-8", "FEED_FORMAT": "json", "FEED_URI": "authors.json"}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").get().strip(),
                "quote": quote.xpath("span[@class='text']/text()").get().strip(),
            }
            yield{
                response.follow(url=self.start_urls[0] + quote.xpath("span/a/@href").get(), callback=self.parse_author)

            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
    
    def parse_author(self, response):
        content = response.xpath("/html//div[@class='author-details']")
        yield {
            "fullname": content.xpath("h3[@class='author-title']/text()").get().strip(),
            "born_date": content.xpath("p/span[@class='author-born-date']/text()").get().strip(),
            "born_location": content.xpath("p/span[@class='author-born-location']/text()").get().strip(),
            "description": content.xpath("div[@class='author-description']/text()").get().strip(),

        }



# run spider
process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()
