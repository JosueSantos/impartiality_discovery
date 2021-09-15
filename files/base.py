# coding: utf-8
import csv
import os
import json

class Base():
    """
    Mapeamento dos arquivos CSV
    """
    
    BASE = 'files/classifier/base.csv'
    TEST = 'files/classifier/base_test.csv'
    TRAINING = 'files/classifier/base_training.csv'

    CRAWLER_PATH = 'files/extractor/crawler'
    BASE_DN = 'files/extractor/base_dn.csv'
    URLS_DN = 'files/extractor/urls_dn.csv'

def getBase(name: str) -> list:
    """
    Transformar os dados dos arquivos CSV em Listas para serem utilizadas no modelo

    Args
    -----
        name: string, Nome de uma das bases de dados BASE, TEST ou TRAINING
        
    Returns
    -----
        dic: list [(text: string, tag: string)], Dados de Texto e suas Tag de categoria
    """
    
    reader = csv.reader(open(name, 'r', encoding='utf-8'), delimiter=';')
    dic = []
    for row in reader:
        dic.append(tuple(row))
    
    return dic

def populateBase():
    """
    Coleta os arquivos JSON obtidos pelo crawler e recolhe o link e o corpo do texto em um arquivo CSV para cada fonte de dados
    
    Também realiza a limpeza da base removendo arquivos inválidos
    """

    deleteFile = []

    with open(Base.BASE_DN, 'w', encoding='utf-8', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
        for filename in os.listdir(Base.CRAWLER_PATH):
            readerCrawler = open(os.path.join(Base.CRAWLER_PATH, filename), 'r', encoding='utf-8')
            try:
                readerJSON = json.load(readerCrawler)

                for data in readerJSON:
                    try:
                        if(data['article']):
                            article = data['article']
                            article = article.rstrip("\n")
                            article = article.strip()

                            spamwriter.writerow([data['link'], article])
                    except:
                        print('row invalid in ' + filename)
            except:
                print('file:' + filename + ' invalid format JSON, will be deleted')
                deleteFile.append(os.path.join(Base.CRAWLER_PATH, filename))
    
    for file in deleteFile:
        os.remove(file)

def getURLsWithContent() -> set:
    """
    Coleta os arquivos JSON obtidos pelo crawler e seleciona as URLs que possuem algum conteúdo
        
    Returns
    -----
        dic: set [string], Lista de URLs processadas
    """
    
    urls_sucess = set()

    for filename in os.listdir(Base.CRAWLER_PATH):
        readerCrawler = open(os.path.join(Base.CRAWLER_PATH, filename), 'r', encoding='utf-8')
        try:
            readerJSON = json.load(readerCrawler)
            for data in readerJSON:
                try:
                    if(data['article']):
                        urls_sucess.add(data['link'])
                except:
                    print('row invalid in ' + filename)
        except:
            print('file:' + filename + ' invalid format JSON')
    
    return urls_sucess

def getURLsForCrawler(urls: str, urls_sucess: set) -> list:
    """
    Transformar os dados dos arquivos CSV em Listas para serem utilizadas no modelo

    Args
    -----
        urls: string, Nome de uma das bases de dados de URLs das fonte disponíveis: URLS_DN
        urls_sucess: set, Lista de URLs já processadas
        
    Returns
    -----
        start_urls: list [string], Lista de URLs para serem processadas no Crawler
    """

    start_urls = []

    reader = open(urls, 'r', encoding='utf-8')
    for row in reader:
        row = row.strip()
        if row not in urls_sucess:
            start_urls.append(row)

    return start_urls