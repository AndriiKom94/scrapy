import scrapy
from ..items import OlxScrapyItem


class OlxSpider(scrapy.Spider):
    name = "laptops"
    start_urls = [
        'https://www.olx.ua/uk/list/q-xiaomi-redmi-5/'
    ]
    page_number = 2
    def parse(self, response):

        items = OlxScrapyItem()

        all_items = response.css('tr.wrap')

        for item in all_items:
            title = item.css('a.detailsLink strong::text').extract()
            price = item.css('p.price strong::text').extract()
            city_date = item.css('p.lheight16 span::text').extract()

            items['title'] = title
            items['price'] = price
            items['city'] = city_date[0]
            items['date'] = city_date[1]

            yield items

        next_page = 'https://www.olx.ua/uk/list/q-xiaomi-redmi-5/?page=' + str(OlxSpider.page_number)

        last_page = response.css('div.pager a span::text').extract()[-2]


        if OlxSpider.page_number <= int(last_page):
            OlxSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)

