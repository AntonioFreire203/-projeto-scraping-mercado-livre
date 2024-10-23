import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/caixa-de-pizza#D[A:caixa%20de%20pizza]"]

    def parse(self, response):
        products = response.css('div.ui-search-result__content')
        
        for product in products:
            yield {
                ##'brand': product.css('span.ui-search-item__group__element::text').get(),
                'title': product.css('h2.ui-search-item__title::text').get(),
                'price': product.css('span.price-tag-fraction::text').get(),
            }