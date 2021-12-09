# coding: utf-8

from classifier.ClassifierService import ClassifierService
from files.base import analytics


"""
Texto
Titulo
Tag Base Verdade
Tag Naive Bayes
Tag Senti Strength
Positive - SentiStrength
Negative - SentiStrength
Neltral - SentiStrength
Link
Origem
Id
Tamanho de frases - word_tokenize
Contagem de palavras neutras - count_neutral_words
Tamanho do Texto em caracteres
"""

classifierService = ClassifierService()

analytics(classifierService)