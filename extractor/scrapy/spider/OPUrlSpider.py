# -*- coding: utf-8 -*-

import scrapy

from extractor.scrapy.UrlItem import UrlItem


class OPUrlSpider(scrapy.Spider):
    """
    Raspador de URLs das Matérias do O Povo
    """

    name = 'o_povo_url'
    allowed_domains = ['opovo.com.br']
    
    start_urls = [
        'https://www.opovo.com.br/noticias/politica/',
    ]

    def parse(self, response):
        print(response.url)
        
        for link in response.css(".listagem a::attr(href)"):
            yield response.follow(link, self.parseMateria)
            
    def parseMateria(self, response):
        link = response.url
        
        urlItem = UrlItem(
			url=link,
		)

        yield urlItem
