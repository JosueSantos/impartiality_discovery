# coding: utf-8

import scrapy
import re
from extractor.ArticleItem import ArticleItem

class DiarioDoNordesteSpider(scrapy.Spider):
    """
    Raspador de Matérias do Diário do Nordeste
    """
    
    name = 'diarioDoNordeste'
    allowed_domains = ['https://diariodonordeste.verdesmares.com.br/']
    start_urls = []

    def parse(self, response):
        TAG_RE = re.compile(r'<[^>]+>|(\s){2,}')
        
        link = response.url
        
        type = response.css(".m-l-article__category__text::text").extract_first()
        type = TAG_RE.sub('', type)

        title = response.css("h1.m-l-article__heading::text").extract_first()
        title = TAG_RE.sub('', title)
        
        subtitle = response.css("h2.m-l-article__subheading::text").extract_first()
        subtitle = TAG_RE.sub('', subtitle)
        
        author = response.css(".m-l-article__author::text").extract_first()
        author = TAG_RE.sub('', author)
        
        date = response.css(".m-l-article__date_created::text").extract_first()
        date = TAG_RE.sub('', date)

        article = response.css(
            ".m-l-article__content p::text, " +
            ".m-l-article__content h2::text, " +
            ".m-l-article__content h1::text"
        ).extract()
        
        articleClean = ''
        for text in article:
            text = TAG_RE.sub('', text)
            text = text.replace(";",":")
            text = text.replace("  "," ")
            text = text.rstrip("\n")
            text = text.strip()
            articleClean += text + " "
        
        if (articleClean):
            yield ArticleItem(
                link = link,
                type = type,
                title = title,
                subtitle = subtitle ,
                article = articleClean,
                author = author,
                date = date,
                origin = "Diario do Nordeste",
            )