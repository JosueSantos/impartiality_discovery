# coding: utf-8

import pickle

from nltk.classify.naivebayes import NaiveBayesClassifier


class ClassifierModel():
    """
    Modelo de Classificador NaiveBayes

    Attributes
    -----
        classifier: NaiveBayesClassifier
        uniqueWords: list [string]
    """
    
    classifier: NaiveBayesClassifier = None
    uniqueWords: list = []

    def __init__(self):
        """
        Construtor do Modelo: Verifica os modelos salvos e o carrega se existir.
        """

        self.getModelSaved()
    
    def getModelSaved(self):
        """
        Carregar Modelo Salvo anteriormente se existir
        """

        try:
            f = open('classifier/export/impartiality_discovery_unique_words.pickle', 'rb')
            self.uniqueWords = pickle.load(f)
            f.close()

            f = open('classifier/export/impartiality_discovery_classifier.pickle', 'rb')
            self.classifier = pickle.load(f)
            f.close()
            
        except:
            print('classifier/impartiality_discovery pickle files not found')
    
    def saveModel(self):
        """
        Salvar Progresso do Modelo em arquivo pickle
        """

        f = open('classifier/export/impartiality_discovery_unique_words.pickle', 'wb')
        pickle.dump(list(self.uniqueWords), f)
        f.close()

        f = open('classifier/export/impartiality_discovery_classifier.pickle', 'wb')
        pickle.dump(self.classifier, f)
        f.close()
    