# coding: utf-8

from classifier.ClassifierService import ClassifierService

print('Impartiality Discovery start...')
classifierService = ClassifierService()

print("Acurácia do Modelo Gerado:")
print( classifierService.accuracy() )

print("Matriz de Confusão")
print( classifierService.confusionMatrix() )

text = 'Não gosto da noite!'
print(text)
print(classifierService.classifySentence(text))

print('---------------------')
classifierService.distributionProbSentence(text)