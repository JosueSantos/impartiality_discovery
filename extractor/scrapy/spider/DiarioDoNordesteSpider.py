# coding: utf-8

import scrapy

from extractor.scrapy.ArticleItem import ArticleItem

from files.base import cleanString


class DiarioDoNordesteSpider(scrapy.Spider):
    """
    Raspador de Matérias do Diário do Nordeste
    """
    
    name = 'diarioDoNordeste'
    allowed_domains = ['diariodonordeste.verdesmares.com.br']
    start_urls = []

    def parse(self, response):
        link = response.url
        print(link)
        
        if (link.find('paywall-') != -1):
            self.crawler.engine.close_spider(self, reason='paywall')
        
        type = response.css(".m-l-article__category__text").extract_first()
        type = cleanString(type)

        title = response.css("h1.m-l-article__heading").extract_first()
        title = cleanString(title)
        
        subtitle = response.css("h2.m-l-article__subheading").extract_first()
        subtitle = cleanString(subtitle)
        
        author = response.css(".m-l-article__author").extract_first()
        author = cleanString(author)

        if(author == ''):
            author = response.css(".m-c-meta a").extract_first()
            author = cleanString(author)
        
        date = response.css(".m-l-article__date_created").extract_first()
        date = cleanString(date)

        if(date == ''):
            date = response.css(".m-c-meta").extract_first()
            date = cleanString(date)
            date = date.split(',')[-1:]
            date = date[0].split('.')[0]
            date = date.strip()

        article = response.css(
            ".m-l-article__content p, " +
            ".m-l-article__content h2, " +
            ".m-l-article__content h1, " + 
            ".m-l-article__content blockquote div"
        ).extract()
        
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
                origin = "Diário do Nordeste",
            )
