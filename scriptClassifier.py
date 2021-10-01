# coding: utf-8

from classifier.ClassifierService import ClassifierService


"""
Realiza o treinamento do modelo apartir dos dados de treinamento e de teste

Salva este modelo com o Pickle
"""

print('Impartiality Discovery start...')
classifierService = ClassifierService(remaker = True)

print('\n\nExecute Jupiter Notebook')