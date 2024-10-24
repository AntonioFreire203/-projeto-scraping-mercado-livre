import scrapy
from datetime import datetime
import re
from typing import List, Dict, Any,Optional

class CentauroSpider(scrapy.Spider):
    name: str = "centauro"
    allowed_domains: List[str] = ["www.centauro.com.br"]
    start_urls: List[str] = ["https://www.centauro.com.br/busca/tenis-corrida-masculino"]
    page_count: int = 1
    max_page: int = 10

    def parse(self, response):
        
        products: List[scrapy.Selector] = response.css('a[data-testid="grid-product-card"]')
        
        for product in products:
            # Extraindo a avaliação do texto
            rating_div: Optional[str] = product.css('div[data-testid="product-rating"]::attr(aria-label)').get()
            rating: Optional[str] = None

            if rating_div:         
                match = re.search(r'avaliado em (\d+(\.\d+)?) de 5 estrelas', rating_div)
                if match:
                    rating:str = match.group(1)

            # Extraindo o brand e name do texto
            brand_and_name:Optional[str] = product.css('p.Typographystyled__Paragraph-sc-bdxvrr-1::text').get()
            if brand_and_name:
                brand, name = self.extract_brand_and_name(brand_and_name)
            else:
                brand, name = None, None
            
            yield {
                'brand': brand,
                'name': name,
                'old_price_reais': product.css('del[data-testid="price-promotion"]::text').get(),
                'new_price_reais': product.css('p[data-testid="price-current"]::text').get(),
                'reviews_rating_number': rating,
                'page_count': self.page_count,
                '_source_name': self.name,
                '_source_link': self.start_urls[0],
                '_data_coleta': datetime.now()
            }
        
        if self.page_count < self.max_page:
            self.page_count += 1
            next_page = f"{self.start_urls[0]}?page={self.page_count}"
            if next_page:
                yield scrapy.Request(url=next_page, callback=self.parse)

    def extract_brand_and_name(self, text:str) :
        parts = text.split(" ", 1)
        if len(parts) >= 2:
            brand = parts[1].split(" ")[0].capitalize()
            return brand, text
        return None, text