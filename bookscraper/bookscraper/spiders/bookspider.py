import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.css('.product_pod')
        
        for book in books:
            yield {
                'url': book.css('h3 a::attr(href)').get(),
                'title': book.css('h3 a::attr(title)').get(),
                'price': book.css('.product_price .price_color::text').get()
            }
            
        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:            
            if 'catalogue/' in next_page:
                next_page_url = self.start_urls[0] + next_page
            else:
                next_page_url = self.start_urls[0] + 'catalogue/' + next_page
                
            yield response.follow(next_page_url, callback=self.parse)
            