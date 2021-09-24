# coding: utf-8

import csv
import os
import re
import random

from classifier.PySentiStrength import PySentiStrength


class Base():
    """
    Mapeamento dos arquivos CSV
    """
    
    BASE = 'files/classifier/base.csv'
    BASE_IMPARTIAL = 'files/classifier/base_impartial.csv'
    BASE_PARTIAL = 'files/classifier/base_partial.csv'

    TEST = 'files/classifier/base_test.csv'
    TRAINING = 'files/classifier/base_training.csv'

    CRAWLER_PATH = 'files/extractor/crawler'

    URLS_DN = 'files/extractor/diarioDoNordeste/urls_dn.csv'
    URLS_G1 = 'files/extractor/g1Ceara/urls_g1.csv'
    URLS_OP = 'files/extractor/oPovo/urls_op.csv'

    URLS_DN_TEMP = 'files/extractor/diarioDoNordeste/urls_dn_temp.csv'
    URLS_G1_TEMP = 'files/extractor/g1Ceara/urls_g1_temp.csv'
    URLS_OP_TEMP = 'files/extractor/oPovo/urls_op_temp.csv'

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

def getSizeDoc(name: str) -> int:
    """
    Retorna o tamanho de um arquivo ou o deleta se estiver vazio
    
    Args
    -----
        name: string, Nome de um arquivo
        
    Returns
    -----
        int, Tamanho do arquivo (os.stat(name).st_size)
    """
    
    size = os.stat(name).st_size
    if (size):
        return size
    else:
        os.remove(name)
        return 0

def populateBase():
    """
    Coleta os arquivos CSV obtidos pelo crawler e recolhe as informações

    Realiza a analise da SentiStrength para cada uma das entradas.

    Com o método PySentiStrength.scoreClassifier() classifica as notícias como imparciais se estiverem em equilibrio entre os pesos positivos e negativos obtidos pelo SentiStrength

    Gera 3 arquivos CSV:
    - Base.BASE
    - Base.BASE_IMPARTIAL
    - Base.BASE_PARTIAL

    Também realiza a limpeza da base removendo arquivos vazios
    """

    deleteFile = []
    pySentiStrength = PySentiStrength()

    csvfile = open(Base.BASE, 'w', encoding='utf-8', newline='')
    spamwriter = csv.writer(csvfile, delimiter=';')
    
    csvfileimpartial = open(Base.BASE_IMPARTIAL, 'w', encoding='utf-8', newline='')
    impartial = csv.writer(csvfileimpartial, delimiter=';')
    
    csvfilepartial = open(Base.BASE_PARTIAL, 'w', encoding='utf-8', newline='')
    partial = csv.writer(csvfilepartial, delimiter=';')
    
    for filename in os.listdir(Base.CRAWLER_PATH):
        fileCsv = os.path.join(Base.CRAWLER_PATH, filename)
        if (os.stat(fileCsv).st_size):
            readerCrawler = csv.reader(open(fileCsv, 'r', encoding='utf-8'), delimiter=';')
            for row in readerCrawler:
                if (row[0] and row[0] != 'article'):
                    score = pySentiStrength.getScore(row[0])
                    
                    spamwriter.writerow([
                        row[0],
                        score['balance'],
                        score['positive'],
                        score['negative'],
                        score['neutral'],
                        row[3],
                        row[4],
                    ])

                    if(score['balance'] == "impartial"):
                        impartial.writerow([ row[0], score['balance'] ])
                    else:
                        partial.writerow([ row[0], score['balance'] ])

        else:
            deleteFile.append(fileCsv)

    csvfile.close()
    csvfileimpartial.close()
    csvfilepartial.close()

    for file in deleteFile:
        os.remove(file)

def toSliceBase(trainingPercentage: int):
    """
    Realiza a partição da Base em treino e teste

    Gerando 2 arquivos:
    - Base.TRAINING
    - Base.TEST
    
    Args
    -----
        trainingPercentage: int, Porcentagem da base gera que vai ser colocada para a base de treinamento, restante será destinado a base de teste
    """

    csvfileimpartial = open(Base.BASE_IMPARTIAL, 'r', encoding='utf-8', newline='')
    csvfilepartial = open(Base.BASE_PARTIAL, 'r', encoding='utf-8', newline='')

    readerImpartial = csv.reader(csvfileimpartial, delimiter=';')
    readerPartial = csv.reader(csvfilepartial, delimiter=';')

    listImpartial = list(readerImpartial)
    listPartial = list(readerPartial)

    impartialSize = len(listImpartial)
    partialSize = len(listPartial)

    trainingImpartial = int(impartialSize * (trainingPercentage/100))
    trainingPartial = int(partialSize * (trainingPercentage/100))

    random.shuffle(listImpartial)
    random.shuffle(listPartial)

    trainImpartial, testImpartial = listImpartial[:trainingImpartial], listImpartial[trainingImpartial:]
    trainPartial, testPartial = listPartial[:trainingPartial], listPartial[trainingPartial:]

    train = trainImpartial + trainPartial
    test = testImpartial + testPartial

    csvfileTrainig = open(Base.TRAINING, 'w', encoding='utf-8', newline='')
    fileTrain = csv.writer(csvfileTrainig, delimiter=';')
    
    for row in train:
        fileTrain.writerow([ row[0], row[1] ])
        
    csvfileTrainig.close()

    csvfileTest = open(Base.TEST, 'w', encoding='utf-8', newline='')
    fileTest = csv.writer(csvfileTest, delimiter=';')

    for row in test:
        fileTest.writerow([ row[0], row[1] ])
        
    csvfileTest.close()

def getURLsWithContent() -> set:
    """
    Coleta os arquivos JSON obtidos pelo crawler e seleciona as URLs que possuem algum conteúdo
        
    Returns
    -----
        dic: set [string], Lista de URLs processadas
    """
    
    urls_sucess = set()

    for filename in os.listdir(Base.CRAWLER_PATH):
        fileCsv = os.path.join(Base.CRAWLER_PATH, filename)
        readerCrawler = csv.reader(open(fileCsv, 'r', encoding='utf-8'), delimiter=';')
        
        for row in readerCrawler:
            if (row[0]):
                urls_sucess.add(row[3])
    
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
        row = row.split(';')[0]
        row = row.strip()
        
        if row not in urls_sucess:
            if ('diariodonordeste' in row):
                idArticle = row.split('-')
                idArticle = idArticle[-1]
                
                if (not any(idArticle in url for url in urls_sucess)):
                    start_urls.append(row)
            else:
                start_urls.append(row)

    return start_urls

def cleanString(text: str) -> str:
    """
    Realiza a limpeza de uma String, removendo Tag's HTML e exceço de espaços

    Args
    -----
        text: string
        
    Returns
    -----
        text: string
    """

    if (text):
        TAG_STYLE_RE = re.compile(r'<style(.+?)</style>')
        text = TAG_STYLE_RE.sub('', text)

        TAG_SCRIPT_RE = re.compile(r'<script(.+?)</script>')
        text = TAG_SCRIPT_RE.sub('', text)

        TAG_COMMENT_RE = re.compile(r'<!--(.+?)-->')
        text = TAG_COMMENT_RE.sub('', text)

        TAG_VIDEO_RE = re.compile(r'\[VIDEO(.+?)\]')
        text = TAG_VIDEO_RE.sub('', text)

        TAG_RE = re.compile(r'<[^>]+>|(\s){2,}')
        text = TAG_RE.sub('', text)
        
        text = text.replace('TAGS','')
        text = text.replace("  "," ")
        text = text.replace('""','"')
        text = text.replace(";",":")
        text = text.replace("\n"," ")
        text = text.replace("\r"," ")
        text = text.replace("\t"," ")
        text = text.strip()
    else:
        text = ''

    return text

def mergeFilesURL(temp: str, origin: str):
    """
    Mescla as URLs capturadas com as URLs contidas na base

    Args
    -----
        temp: string, Caminho do arquivo temporario gerado pelo crawler
        origin: string, Caminho do arquivo da base de URLs
    """
    
    urlsRemove = [
        'url',
        'https://diariodonordeste.verdesmares.com.br/pontopoder',
    ]

    with open(temp,'r+', encoding='utf-8', newline='') as file_temp, open(origin,'r+', encoding='utf-8', newline='') as file_origin:
        data = set()
        for line in file_temp:
            if (
                line in data or
                line.strip() in urlsRemove or
                line[:4] != 'http' or
                line.find('/video/') != -1
            ):
                continue

            data.add(line)

        for line in file_origin:
            if (
                line in data or
                line.strip() in urlsRemove or
                line[:4] != 'http' or
                line.find('/video/') != -1
            ):
                continue

            data.add(line)
        
        """
        Operação de segurança para Existir um backup de Dados em caso de erros
        """

        file_temp.seek(0)
        file_temp.truncate()

        for line in data:
            file_temp.write(line)
        
        """
        Agrupamento de informações
        """
        
        file_origin.seek(0)
        file_origin.truncate()

        count = 0

        for line in data:
            count += 1
            file_origin.write(line)
        
        print(str(count) + " lines in " + origin)
    
    os.remove(temp)

def mergeFilesCrawler(temp: str, origin: str):
    """
    Mescla as arquivos capturados pelo crawler

    Args
    -----
        temp: string, Caminho do arquivo que será deletado
        origin: string, Caminho do arquivo que será unido ao outro
    """
    
    dataRemove = [
        'article;author;date;link;origin;subtitle;title;type',
    ]

    with open(temp,'r+', encoding='utf-8', newline='') as file_temp, open(origin,'r+', encoding='utf-8', newline='') as file_origin:
        data = set()
        for line in file_temp:
            if (
                line in data or
                line.strip() in dataRemove
            ):
                continue

            data.add(line)

        for line in file_origin:
            if (
                line in data or
                line.strip() in dataRemove
            ):
                continue

            data.add(line)
        
        """
        Operação de segurança para Existir um backup de Dados em caso de erros
        """

        file_temp.seek(0)
        file_temp.truncate()

        for line in data:
            file_temp.write(line)
        
        """
        Agrupamento de informações
        """
        
        file_origin.seek(0)
        file_origin.truncate()

        count = 0

        for line in data:
            count += 1
            file_origin.write(line)
        
        print(str(count) + " lines in " + origin)
    
    os.remove(temp)

def reduceFilesCrawler():
    filesCrawler = os.listdir(Base.CRAWLER_PATH)
    for i in range(0, len(filesCrawler), 2):
        if i+1 < len(filesCrawler):
            fileCsvTemp = os.path.join(Base.CRAWLER_PATH, filesCrawler[i])
            fileCsv = os.path.join(Base.CRAWLER_PATH, filesCrawler[i+1])
            
            mergeFilesCrawler(fileCsvTemp, fileCsv)
