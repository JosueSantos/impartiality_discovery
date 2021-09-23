# coding: utf-8

import scrapy


class UrlItem(scrapy.Item):
    """
    Unidade básica dos arquivos de URL
    """
    
    url = scrapy.Field()
    