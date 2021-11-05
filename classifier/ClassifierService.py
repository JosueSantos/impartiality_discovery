# coding: utf-8

import nltk
from nltk.metrics import ConfusionMatrix

from files.base import Base, getBase
from classifier.ClassifierController import ClassifierController


class ClassifierService():
    """
    Serviço para gerenciar o Classificador
    """
    
    classifierController = ClassifierController()

    def __init__(self, remaker = False):
        """
        Realiza o download ou update do pacote NLTK

        O preparo dos dados e o treinamento do modelo
        """
        
        nltk.download('rslp')

        if(self.classifierController.notExistClassifier() | remaker):
            self.classifierController.buildBase( getBase(Base.TRAINING) )
            self.classifierController.train()

            self.classifierController.classifierModel.saveModel()

    def accuracy(self, groundTruth = False):
        """
        Calcula a precisão do modelo comparado com a base de teste
        
        Returns
        -----
            accuracy: float, Porcentagem de precisão do modelo
        """
        
        classifierTest = ClassifierController()
        if (groundTruth):
            classifierTest.buildBase( getBase(Base.BASE_GROUND_TRUTH) )
        else:
            classifierTest.buildBase( getBase(Base.TEST) )
        
        accuracy = self.classifierController.accuracy(classifierTest.base)
        
        return(accuracy)
    
    def confusionMatrix(self, groundTruth = False) -> ConfusionMatrix:
        """
        Calcula uma tabela que permite extrair métricas que auxiliam na avaliação de modelos
        
        Returns
        -----
            matriz: ConfusionMatrix, Retorna uma matriz de acertos e erros do modelo
        """
        
        classifierTest = ClassifierController()
        if (groundTruth):
            classifierTest.buildBase( getBase(Base.BASE_GROUND_TRUTH) )
        else:
            classifierTest.buildBase( getBase(Base.TEST) )

        expected = []
        predicted = []

        for (phrase, tag) in classifierTest.base:
            resultado = self.classifierController.classifierModel.classifier.classify(phrase)

            predicted.append(resultado)
            expected.append(tag)

        matriz = ConfusionMatrix(expected, predicted)
        
        return(matriz)
    
    def classifySentence(self, text) -> str:
        """
        Submete um texto para a avaliação do modelo

        Args
        -----
            text: string
        
        Returns
        -----
            tag: string, Retorna a Tag que o modelo identificou para o texto enviado
        """
        
        textClean = self.classifierController.prepareSentence(text)
        tag = self.classifierController.classifierModel.classifier.classify(textClean)
        
        return(tag)

    def distributionProbSentence(self, text) -> dict:
        """
        Submete um texto para a avaliação do modelo

        Realiza o print da distribuição de probabilidades entre as tags do modelo e retorna esta mesma distribuição

        Args
        -----
            text: string
        
        Returns
        -----
            dict: ([tag] = Porcentagem), Retorna a lista de probabilidades para cada uma das tags do modelo
        """
        
        distribution = self.classifierController.analyticsText(text)
        dict = {}
        for tag in distribution.samples():
            dict[tag] = distribution.prob(tag)
            
            print(tag , ": " ,dict[tag])

        return dict
    
    def getUnique(self, base):
        baseCleaning = self.classifierController.baseCleaning(getBase(base))
        return self.classifierController.findUniqueWords(baseCleaning)
