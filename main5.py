import scrapy
from scrapy.crawler import CrawlerProcess


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    custom_settings = {
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_FORMAT": "json",
        "FEED_URI": "quotes.json",
    }
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            yield {
                "tags": quote.xpath(".//div[@class='tags']/a/text()").extract(),
                "author": quote.xpath(".//span/small/text()").get(),
                "quote": quote.xpath(".//span[@class='text']/text()").get(),
            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield response.follow(next_link, callback=self.parse)

class AuthorsSpider(scrapy.Spider):
    name = "authors"
    custom_settings = {
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_FORMAT": "json",
        "FEED_URI": "authors.json",
    }
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/authors"]

    def parse(self, response):
        for author in response.xpath("//div[@class='author-details']"):
            yield {
                "name": author.xpath(".//h3/text()").get(),
                "birth_date": author.xpath(".//span[@class='author-born-date']/text()").get(),
                "birth_place": author.xpath(".//span[@class='author-born-location']/text()").get(),
                "description": author.xpath(".//div[@class='author-description']/text()").get(),
            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield response.follow(next_link, callback=self.parse)


if __name__ == "__main__":

    # run spider
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.crawl(AuthorsSpider)
    process.start()

    