# coding: utf-8

from classifier.ClassifierService import ClassifierService
from files.base import populateNaiveBayes


classifierService = ClassifierService()

populateNaiveBayes(classifierService)
