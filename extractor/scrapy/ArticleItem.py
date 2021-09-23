# coding: utf-8

import scrapy


class ArticleItem(scrapy.Item):
    """
    Unidade básica dos dados necessários para se obter de um artigo jornalístico
    """
    
    link = scrapy.Field()
    type = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    article = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    origin = scrapy.Field()
