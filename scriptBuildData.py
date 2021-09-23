# coding: utf-8

from files.base import populateBase, toSliceBase


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

populateBase()

"""
Realiza a partição da Base em treino e teste

Gerando 2 arquivos:
 - Base.TRAINING
 - Base.TEST
"""

toSliceBase(30)
