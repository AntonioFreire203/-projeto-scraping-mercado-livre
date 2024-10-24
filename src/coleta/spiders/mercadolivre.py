import scrapy
from datetime import datetime
import re
from typing import List, Dict, Any

class MercadolivreSpider(scrapy.Spider):
    name: str = "mercadolivre"
    allowed_domains: List[str] = ["lista.mercadolivre.com.br"]
    start_urls:List[str] = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]
    page_count:int = 1
    max_pages:int = 10

    def parse(self, response):
        products: List[scrapy.Selector] = response.css('div.ui-search-result__content')

        for product in products:
            prices: List[str] = product.css('span.andes-money-amount__fraction::text').getall()
            cents: List[str] = product.css('span.andes-money-amount__cents::text').getall()
            
            yield {
                'brand': product.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get(),
                'name': product.css('h2.ui-search-item__title::text').get(),
                'old_price_reais': prices[0] if len(prices) > 0 else None,
                'old_price_centavos': cents[0] if len(cents) > 0 else None,
                'new_price_reais': prices[1] if len(prices) > 1 else None,
                'new_price_centavos': cents[1] if len(cents) > 1 else None,
                'reviews_rating_number': product.css('span.ui-search-reviews__rating-number::text').get(),
                'reviews_amount': product.css('span.ui-search-reviews__amount::text').get(),
                'page_count': self.page_count,
                '_source_name': self.name,
                '_source_link': self.start_urls[0],
                '_data_coleta': datetime.now()
            }

        if self.page_count < self.max_pages:
            next_page: str = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)
