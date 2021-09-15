# coding: utf-8

from scrapy.crawler import CrawlerProcess
from random import random

from files.base import Base, getURLsForCrawler, getURLsWithContent, populateBase
from extractor.DiarioDoNordesteSpider import DiarioDoNordesteSpider

class ExtractorService():

    def buildData():
        """
        Executa os Cralwers necessários para a captura dos dados
        
        Gera os arquivos CSV com o link e o corpo dos artigos: dase_dn.csv
        """

        urls_sucess = getURLsWithContent()
        start_urls_DN = getURLsForCrawler(Base.URLS_DN, urls_sucess)

        key = int(random() * 100000)
        filename = "/data" + str(key) +".json"

        processDN = CrawlerProcess(settings={
            "FEEDS": {
                Base.CRAWLER_PATH + filename : {"format": "json"},
            },
        })

        processDN.crawl(DiarioDoNordesteSpider, start_urls=start_urls_DN)
        processDN.start()

        print('-------------------------------')
        print('URLs crawler with sucess are ' + str(len(urls_sucess)))
        print('remaining URLs in base: ' + str(len(start_urls_DN)))
        print('-------------------------------')

        if(len(start_urls_DN) > 0):
            print('run again ExtractorService.buildData() if you find it necessary')
        
        populateBase()