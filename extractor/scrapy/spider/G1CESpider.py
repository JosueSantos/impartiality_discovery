# coding: utf-8

import scrapy

from extractor.scrapy.ArticleItem import ArticleItem

from files.base import cleanString


class G1CESpider(scrapy.Spider):
    """
    Raspador de Matérias do G1
    """
    
    name = 'g1Ceara'
    allowed_domains = ['g1.globo.com']
    start_urls = []

    def parse(self, response):
        link = response.url
        print(link)
        
        type = link.split('/')[3]
        type = cleanString(type)

        title = response.css(".content-head__title").extract_first()
        title = cleanString(title)

        if (title == ''):
            title = response.css(".materia-titulo .entry-title").extract_first()
            title = cleanString(title)
        
        subtitle = response.css(".content-head__subtitle").extract_first()
        subtitle = cleanString(subtitle)

        if (subtitle == ''):
            subtitle = response.css(".materia-titulo h2").extract_first()
            subtitle = cleanString(subtitle)
        
        author = response.css(".content-publication-data__from::attr(title)").extract_first()
        author = cleanString(author)

        if (author == ''):
            author = response.css(".author fn").extract_first()
            author = cleanString(author)

        date = response.css(".content-publication-data__updated time").extract_first()
        date = cleanString(date)

        if (date == ''):
            date = response.css(".materia-cabecalho published").extract_first()
            date = cleanString(date)

        article = response.css(
            ".mc-article-body article p, " +
            ".mc-article-body article h2, " +
            ".mc-article-body article h1"
        ).extract()
        
        articleClean = ''
        for text in article:
            text = cleanString(text)
            articleClean += text + " "
        
        articleClean = articleClean.replace("  "," ")
        articleClean = articleClean.strip()

        if (articleClean == ''):
            article = response.css(".materia-conteudo p").extract()
            articleClean = ''
            for text in article:
                text = cleanString(text)
                articleClean += text + " "
            
            articleClean = articleClean.replace("  "," ")
            articleClean = articleClean.strip()
        
        if (articleClean):
            articleClean = title + ' - ' + subtitle + ' - ' + articleClean
            articleClean = cleanString(articleClean)

            yield ArticleItem(
                link = link,
                type = type,
                title = title,
                subtitle = subtitle ,
                article = articleClean,
                author = author,
                date = date,
                origin = "G1 Ceará",
            )
