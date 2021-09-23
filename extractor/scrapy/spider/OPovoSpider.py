# coding: utf-8

import scrapy

from extractor.scrapy.ArticleItem import ArticleItem

from files.base import cleanString


class OPovoSpider(scrapy.Spider):
    """
    Raspador de Matérias do O Povo
    """
    
    name = 'oPovo'
    allowed_domains = ['opovo.com.br']
    start_urls = []

    def parse(self, response):
        link = response.url
        if(response.css("body") != []):
            print(link)
        
        type = link.split('/')[3]
        type = cleanString(type)

        title = response.css(".topo-materia .titulo").extract_first()
        title = cleanString(title)

        if (title == ''):
            title = response.css("header .tit-noticia").extract_first()
            title = cleanString(title)
        
        subtitle = response.css(".topo-materia .subtitulo").extract_first()
        subtitle = cleanString(subtitle)

        if (subtitle == ''):
            subtitle = response.css("header .abre-noticia").extract_first()
            subtitle = cleanString(subtitle)
        
        author = response.css(".topo-materia .caixa-status .autor span a").extract_first()
        author = cleanString(author)

        date = response.css(".topo-materia .caixa-status .horario").extract_first()
        date = cleanString(date)

        if (date == ''):
            date = response.css("header .toolbar .data").extract_first()
            date = cleanString(date)

        article = response.css(
            ".texto-princinpal p.texto, " +
            ".texto-princinpal h2, " +
            ".texto-princinpal h1, " +
            "article.conteudo .conteudo-interna p.texto"
        ).extract()
        
        articleClean = ''
        for text in article:
            text = cleanString(text)
            articleClean += text + " "
        
        articleClean = articleClean.replace("  "," ")
        articleClean = articleClean.strip()

        if (articleClean == ''):
            article = response.css(
                ".texto-princinpal p, " +
                "article.conteudo .conteudo-interna"
            ).extract()
            
            articleClean = ''
            for text in article:
                text = cleanString(text)
                articleClean += text + " "
            
            articleClean = articleClean.replace("  "," ")
            articleClean = articleClean.strip()

        if (articleClean):
            yield ArticleItem(
                link = link,
                type = type,
                title = title,
                subtitle = subtitle ,
                article = articleClean,
                author = author,
                date = date,
                origin = "O Povo",
            )
            