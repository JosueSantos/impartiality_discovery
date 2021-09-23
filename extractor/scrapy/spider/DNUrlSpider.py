# -*- coding: utf-8 -*-

import scrapy

from extractor.scrapy.UrlItem import UrlItem


class DNUrlSpider(scrapy.Spider):
    """
    Raspador de URLs das Matérias do Diário do Nordeste
    """

    name = 'diario_nordeste_url'
    allowed_domains = ['diariodonordeste.verdesmares.com.br']

    key = '0'
    editoria = 'pontopoder'
    start_urls = [
        'https://diariodonordeste.verdesmares.com.br/'+editoria+'?page='+key+'0',
        'https://diariodonordeste.verdesmares.com.br/'+editoria+'?page='+key+'1',
        'https://diariodonordeste.verdesmares.com.br/'+editoria+'?page='+key+'2',
        'https://diariodonordeste.verdesmares.com.br/'+editoria+'?page='+key+'3',
        'https://diariodonordeste.verdesmares.com.br/'+editoria+'?page='+key+'4',
        'https://diariodonordeste.verdesmares.com.br/'+editoria+'?page='+key+'5',
        'https://diariodonordeste.verdesmares.com.br/'+editoria+'?page='+key+'6',
        'https://diariodonordeste.verdesmares.com.br/'+editoria+'?page='+key+'7',
        'https://diariodonordeste.verdesmares.com.br/'+editoria+'?page='+key+'8',
        'https://diariodonordeste.verdesmares.com.br/'+editoria+'?page='+key+'9',
    ]

    def parse(self, response):
        print(response.url)
        
        for link in response.css("a.m-c-teaser__link::attr(href)"):
            yield response.follow(link, self.parseMateria)
            
    def parseMateria(self, response):
        link = response.url

        urlItem = UrlItem(
			url=link,
		)
        
        yield urlItem
