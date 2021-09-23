# coding: utf-8

from extractor.ExtractorService import ExtractorService


"""
Executa os Cralwers necessários para a captura dos dados nos sites Diário do Nordeste, G1 e O Povo

Gera os arquivos CSV com as informações dos artigos e salva no caminho: files/extractor/crawler/

Esta etapa deve se repetir até ser capturada uma grande quantidade de dados
"""

ExtractorService.extractData()
