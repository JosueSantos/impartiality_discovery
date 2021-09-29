# coding: utf-8

from classifier.ClassifierService import ClassifierService


"""
Realiza o treinamento do modelo apartir dos dados de treinamento e de teste

Salva este modelo com o Pickle
"""

print('Impartiality Discovery start...')
classifierService = ClassifierService(ramaker= True)

print("Acurácia do Modelo Gerado:")
print( classifierService.accuracy() )

print("Matriz de Confusão")
print( classifierService.confusionMatrix() )
