# coding: utf-8

from classifier.ClassifierService import ClassifierService
from files.base import populateNaiveBayes

"""
Realiza a analise do modelo Naive Bayes para cada uma das Notícias da base.

Gera um arquivo CSV:
 - Base.TRAINING_NAIVE_BAYES
"""

classifierService = ClassifierService()

populateNaiveBayes(classifierService)
