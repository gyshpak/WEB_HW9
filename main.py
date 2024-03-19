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
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            author_url = quote.xpath("span/a/@href").get()
            yield response.follow(url=response.urljoin(author_url), callback=self.parse_author)

    def parse_author(self, response):
        author_name = response.xpath("//h3/text()").get()
        birth_date = response.xpath("//span[@class='author-born-date']/text()").get()
        birth_place = response.xpath("//span[@class='author-born-location']/text()").get()
        description = response.xpath("//div[@class='author-description']/text()").get()
        yield {
            "name": author_name,
            "birth_date": birth_date,
            "birth_place": birth_place,
            "description": description,
        }


if __name__ == "__main__":

    # run spider
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.crawl(AuthorsSpider)
    process.start()