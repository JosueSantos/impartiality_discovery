# coding: utf-8

from extractor.ExtractorService import ExtractorService


"""
Executa os Cralwers necessários para a captura das urls das notícias dos sites Diário do Nordeste, G1 e O Povo

Remove as URLs duplicadas e salva o progresso nos arquivos CSV:
 - Base.URLS_DN
 - Base.URLS_G1
 - Base.URLS_OP

Esta etapa deve se repetir diariamente até ser capturada uma grande quantidade de urls
"""

ExtractorService.updateURLs()
