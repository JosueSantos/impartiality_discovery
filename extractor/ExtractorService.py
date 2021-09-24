# coding: utf-8

from random import random
from twisted.internet import defer, reactor
from scrapy.crawler import CrawlerRunner

from files.base import Base, getSizeDoc, getURLsForCrawler, getURLsWithContent, mergeFilesURL, reduceFilesCrawler

from extractor.scrapy.spider.OPUrlSpider import OPUrlSpider
from extractor.scrapy.spider.G1UrlSpider import G1UrlSpider
from extractor.scrapy.spider.DNUrlSpider import DNUrlSpider

from extractor.scrapy.spider.DiarioDoNordesteSpider import DiarioDoNordesteSpider
from extractor.scrapy.spider.G1CESpider import G1CESpider
from extractor.scrapy.spider.OPovoSpider import OPovoSpider


class ExtractorService():
    """
    Serviço responsável pela gerência dos Crawlers
    """

    def extractData():
        """
        Executa os Cralwers necessários para a captura dos dados
        
        Gera os arquivos CSV com as informações dos artigos e salva no caminho: files/extractor/crawler/
        """

        key = int(random() * 100000)
        filename = "/data" + str(key) +".csv"

        runner = CrawlerRunner(settings={
            "FEEDS": {
                Base.CRAWLER_PATH + filename : {"format": "csv"},
            },
            "FEED_EXPORTERS": {
                'csv': 'extractor.scrapy.CsvCustomSeparator.CsvCustomSeparator'
            },
        })

        urls_sucess = getURLsWithContent()

        start_urls_dn = getURLsForCrawler(Base.URLS_DN, urls_sucess)
        DiarioDoNordesteSpider.start_urls = start_urls_dn
        runner.crawl(DiarioDoNordesteSpider)

        start_urls_g1 = getURLsForCrawler(Base.URLS_G1, urls_sucess)
        G1CESpider.start_urls = start_urls_g1
        runner.crawl(G1CESpider)
        
        start_urls_op = getURLsForCrawler(Base.URLS_OP, urls_sucess)
        OPovoSpider.start_urls = start_urls_op
        runner.crawl(OPovoSpider)
        
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()

        print('-------------------------------')
        urls_sucess = getURLsWithContent()
        print('URLs crawler with sucess are ' + str(len(urls_sucess)))

        start_urls_dn = getURLsForCrawler(Base.URLS_DN, urls_sucess)
        start_urls_g1 = getURLsForCrawler(Base.URLS_G1, urls_sucess)
        start_urls_op = getURLsForCrawler(Base.URLS_OP, urls_sucess)

        print('remaining URLs in base DN: ' + str(len(start_urls_dn)))
        print('remaining URLs in base G1: ' + str(len(start_urls_g1)))
        print('remaining URLs in base OP: ' + str(len(start_urls_op)))

        size = getSizeDoc(Base.CRAWLER_PATH + filename)
        if(size):
            print('\nCaptured new articles\n')
            reduceFilesCrawler()
        else:
            print('\nNot found new articles')
            
        print('-------------------------------')
    
    def updateURLs():
        """
        Busca novas URLs de notícias para atualizar a base
        """
        
        runnerDN = CrawlerRunner(settings={ "FEEDS": { Base.URLS_DN_TEMP : {"format": "csv"}, } })
        runnerG1 = CrawlerRunner(settings={ "FEEDS": { Base.URLS_G1_TEMP : {"format": "csv"}, } })
        runnerOP = CrawlerRunner(settings={ "FEEDS": { Base.URLS_OP_TEMP : {"format": "csv"}, } })

        @defer.inlineCallbacks
        def crawl():
            yield runnerDN.crawl(DNUrlSpider)
            yield runnerG1.crawl(G1UrlSpider)
            yield runnerOP.crawl(OPUrlSpider)

            reactor.stop()

        crawl()
        reactor.run()
        
        print('Merge Files URLs DN')
        mergeFilesURL(Base.URLS_DN_TEMP, Base.URLS_DN)

        print('Merge Files URLs G1')
        mergeFilesURL(Base.URLS_G1_TEMP, Base.URLS_G1)

        print('Merge Files URLs OP')
        mergeFilesURL(Base.URLS_OP_TEMP, Base.URLS_OP)
