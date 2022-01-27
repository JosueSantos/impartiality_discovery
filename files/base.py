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
    BASE_ANALYTICS = 'files/classifier/base_analytics.csv'

    FILE_FINAL = 'files/base_analytics_final.csv'

    BASE_IMPARTIAL = 'files/classifier/base_impartial.csv'
    BASE_PARTIAL = 'files/classifier/base_partial.csv'

    BASE_GROUND_TRUTH = 'files/classifier/base_ground_truth.csv'
    URL_GROUND_TRUTH = 'files/ground_truth.csv'

    TEST = 'files/classifier/base_test.csv'
    TRAINING = 'files/classifier/base_training.csv'

    TRAINING_NAIVE_BAYES = 'files/classifier/base_training_naive_bayes.csv'

    CRAWLER_PATH = 'files/extractor/crawler'

    URLS_DN = 'files/extractor/diarioDoNordeste/urls_dn.csv'
    URLS_G1 = 'files/extractor/g1Ceara/urls_g1.csv'
    URLS_OP = 'files/extractor/oPovo/urls_op.csv'

    URLS_DN_TEMP = 'files/extractor/diarioDoNordeste/urls_dn_temp.csv'
    URLS_G1_TEMP = 'files/extractor/g1Ceara/urls_g1_temp.csv'
    URLS_OP_TEMP = 'files/extractor/oPovo/urls_op_temp.csv'

def getBase(name: str, allFile = False) -> list:
    """
    Transformar os dados dos arquivos CSV em Listas para serem utilizadas no modelo

    Args
    -----
        name: string, Nome de uma das bases de dados BASE, TEST ou TRAINING
        allFile [opcional]: boolean, True para retornar todas as colunas, False para retornar apenas as duas primeiras colunas em formato de tupla
        
    Returns
    -----
        dic: list [(string, string)], Dados de Texto e suas Tag de categoria
    """
    
    reader = csv.reader(open(name, 'r', encoding='utf-8'), delimiter=';')
    dic = []
    for row in reader:
        if (allFile):
            dic.append(tuple(row[0:]))
        else:
            dic.append(tuple(row[0:2]))
    
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

def populateBase(update = True):
    """
    Coleta os arquivos CSV obtidos pelo crawler e recolhe as informações

    Realiza a analise da SentiStrength para cada uma das entradas.

    Com o método PySentiStrength.scoreClassifier() classifica as notícias como imparciais de acordo com os pesos positivos e negativos obtidos pelo SentiStrength

    Gera 4 arquivos CSV:
    - Base.BASE
    - Base.BASE_IMPARTIAL
    - Base.BASE_PARTIAL
    - Base.BASE_GROUND_TRUTH

    Também realiza a limpeza da base removendo arquivos vazios
    
    Args
    -----
        update [opcional]: boolean, True para adicionar novas informações mantendo as anteriores, False para apagar as informações anteriores e carregar novas
    """

    deleteFile = []
    pySentiStrength = PySentiStrength()

    base = []
    id_key = 0
    type_file = 'w'
    if (update):
        try:
            base = list(zip(*getBase(Base.BASE, allFile = True)))
            id_key = int(base[7][-1])
            type_file = 'a+'
            
            print("Updating Base...")
            print(id_key)
        except:
            print("Creating new base...")

    csvfile = open(Base.BASE, type_file, encoding='utf-8', newline='')
    spamwriter = csv.writer(csvfile, delimiter=';')
    
    csvfileimpartial = open(Base.BASE_IMPARTIAL, type_file, encoding='utf-8', newline='')
    impartial = csv.writer(csvfileimpartial, delimiter=';')
    
    csvfilepartial = open(Base.BASE_PARTIAL, type_file, encoding='utf-8', newline='')
    partial = csv.writer(csvfilepartial, delimiter=';')

    groundTruth = list(zip(*getBase(Base.URL_GROUND_TRUTH)))
    csvGroundTruth = open(Base.BASE_GROUND_TRUTH, type_file, encoding='utf-8', newline='')
    baseGroundTruth = csv.writer(csvGroundTruth, delimiter=';')

    for filename in os.listdir(Base.CRAWLER_PATH):
        fileCsv = os.path.join(Base.CRAWLER_PATH, filename)
        if (os.stat(fileCsv).st_size):
            readerCrawler = csv.reader(open(fileCsv, 'r', encoding='utf-8'), delimiter=';')
            for row in readerCrawler:
                if (row[0] and row[0] != 'article'):
                    if(not base or row[3] not in base[5]):
                        id_key += 1
                        score = pySentiStrength.getScore(row[0])
                    
                        spamwriter.writerow([
                            row[0],
                            score['balance'],
                            score['positive'],
                            score['negative'],
                            score['neutral'],
                            row[3],
                            row[4],
                            id_key,
                            score['length'],
                            score['count_neutral_words'],
                        ])

                        if(row[3] in groundTruth[1]):
                            key = groundTruth[1].index(row[3])
                            baseGroundTruth.writerow([
                                row[0],
                                groundTruth[0][key],
                                id_key,
                                score['length'],
                                score['count_neutral_words'],
                            ])
                        else:
                            if(score['balance'] == "impartial"):
                                impartial.writerow([ row[0], score['balance'], id_key ])
                            else:
                                partial.writerow([ row[0], score['balance'], id_key ])

        else:
            deleteFile.append(fileCsv)

    csvfile.close()
    csvfileimpartial.close()
    csvfilepartial.close()

    for file in deleteFile:
        os.remove(file)

def toSliceBase(trainingPercentage: int):
    """
    Realiza a partição da Base em Treino e Teste

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

    # if(partialSize < impartialSize):
    #     sizeTraining = partialSize
    # else:
    #     sizeTraining = impartialSize


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
        text = text.replace('""','')
        text = text.replace("''","")
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
    """
    Realiza uma varredura no caminho CRAWLER_PATH
    Capturando de dois em dois o caminho dos arquivos e chamando a função MergeFilesCrawler
    """
    
    filesCrawler = os.listdir(Base.CRAWLER_PATH)
    for i in range(0, len(filesCrawler), 2):
        if i+1 < len(filesCrawler):
            fileCsvTemp = os.path.join(Base.CRAWLER_PATH, filesCrawler[i])
            fileCsv = os.path.join(Base.CRAWLER_PATH, filesCrawler[i+1])
            
            mergeFilesCrawler(fileCsvTemp, fileCsv)

def populateNaiveBayes(classifierService):
    """
    Realiza a analise do modelo Naive Bayes para cada uma das Notícias da base.

    Gera um arquivo CSV:
    - Base.TRAINING_NAIVE_BAYES
    """
    csvNaiveBayes = open(Base.TRAINING_NAIVE_BAYES, 'w', encoding='utf-8', newline='')
    baseNaiveBayes = csv.writer(csvNaiveBayes, delimiter=';')
    
    readerCrawler = csv.reader(open(Base.TRAINING, 'r', encoding='utf-8'), delimiter=';')
    for row in readerCrawler:
        type = classifierService.classifySentence(row[0])
        print(type)
        print(len(row[0]))
        baseNaiveBayes.writerow([ row[0], type ])
        
    csvNaiveBayes.close()

def analytics(classifierService):
    csvAnalytics = open(Base.BASE_ANALYTICS, 'w', encoding='utf-8', newline='')
    baseAnalytics = csv.writer(csvAnalytics, delimiter=';')

    readBASE = csv.reader(open(Base.BASE, 'r', encoding='utf-8'), delimiter=';')
    base = list(readBASE)
    countBase = len(base)

    groundTruth = list(zip(*getBase(Base.URL_GROUND_TRUTH)))

    for row in base:
        rowAnalytics = []

        countBase = countBase - 1
        textSize = len(row[0])
        title = row[0].split(' -')[0]

        tagNaiveBayes = classifierService.classifySentence(row[0])

        tagTruth = None

        if(row[5] in groundTruth[1]):
            key = groundTruth[1].index(row[5])
            tagTruth = groundTruth[0][key]
        
        if(row[5]):
            rowAnalytics = [
                row[0], # Text
                title,
                tagTruth,
                tagNaiveBayes,
                row[1], # Tag - SentiStrength
                row[2], # positive - SentiStrength
                row[3], # negative - SentiStrength
                row[4], # neltral - SentiStrength
                row[5], # link
                row[6], # origem
                row[7], # id
                row[8], # length - word_tokenize
                row[9], # count_neutral_words
                textSize
            ]
            
            baseAnalytics.writerow( rowAnalytics )

            print(str(countBase) + "     -     " + title)

    csvAnalytics.close()
    
