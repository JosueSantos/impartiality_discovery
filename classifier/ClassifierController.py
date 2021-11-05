# coding: utf-8

import re
import nltk
from nltk.classify.naivebayes import NaiveBayesClassifier
from nltk.collections import LazyMap
from nltk.stem.rslp import RSLPStemmer
from nltk.corpus import stopwords
from nltk.probability import DictionaryProbDist, FreqDist

from classifier.ClassifierModel import ClassifierModel


class ClassifierController():
    """
    Controlador de todas as ações do classificador

    Attributes
    -----
        stopWords: list [string]
        base: LazyMap
        stemmer: RSLPStemmer
        classifierModel: ClassifierModel
    """
    
    stopWords = []
    base: LazyMap = None

    stemmer: RSLPStemmer = RSLPStemmer()
    classifierModel: ClassifierModel = ClassifierModel()

    def __init__(self):
        """
        Construtor: Carregar a lista de stopwords na lingua portuguesa e removido desta lista a sentença NÃO pelo seu impacto no sentido de qualquer frase
        """

        self.stopwords = set(stopwords.words('portuguese'))
        self.stopwords.discard('não')
    
    def notExistClassifier(self) -> bool:
        """
        Verifica a existência de um modelo salvo
        
        Returns
        -----
            boolean: True, se não existir
        """

        return self.classifierModel.classifier == None
    
    def buildBase(self, document: dict):
        """
        Realiza o pré-processamento completo da Base de Dados

        Args
        -----
            document: dict( { text, tag } )
        """

        baseCleaning = self.baseCleaning(document)
        self.findUniqueWords(baseCleaning)

        self.base = nltk.classify.apply_features(self.extractWords, baseCleaning)
    
    def train(self):
        """
        Realiza o treinamento do Modelo e registra no ClassifierModel   
        """

        self.classifierModel.classifier = NaiveBayesClassifier.train(self.base)
    
    def accuracy(self, baseTest: dict):
        """
        Calcula a precisão do modelo baseado em uma base de teste

        Args
        -----
            baseTest: dict( { text, tag } )
        
        Returns
        -----
            accuracy: float, Porcentagem de precisão do modelo
        """

        return nltk.classify.accuracy(self.classifierModel.classifier, baseTest)
    
    def textCleaning(self, text: str) -> list:
        """
        Remoção de Pontuação, Links, StopWords e Prefixos e Sufixos de um único texto

        Args
        -----
            text: String
        
        Returns
        -----
            phrasesClean: list [string], Lista das palavras do texto
        """

        phrasesClean = []
        for (words) in text.split():
            words = re.sub(r'[^\w\s$]|http\S+','', words).lower()
            withStem = [ p for p in words.split() if p not in self.stopWords ]
            if(withStem):
                phrasesClean.append(str(self.stemmer.stem(withStem[0])))
        
        return phrasesClean

    def prepareSentence(self, text:str) -> dict:
        """
        Realiza a preparação de um texto para a analise do Classificador

        Args
        -----
            text: String
        
        Returns
        -----
            extractWords: dict, Mapeamento das UniqueWords encontradas no texto
        """

        testStem = self.textCleaning(text)

        return self.extractWords(testStem)

    def analyticsText(self, text: str) -> DictionaryProbDist:
        """
        Retorna as Probabilidades descobertas sobre determinado texto

        Args
        -----
            text: String
        
        Returns
        -----
            distribution: DictionaryProbDist, Distribuição da probabilidade entre as Labels disponiveis
        """
        
        newPhrase = self.prepareSentence(text)

        return self.classifierModel.classifier.prob_classify(newPhrase)
    
    def baseCleaning(self, document: dict) -> list:
        """
        Remoção de Pontuação, Links, StopWords e Prefixos e Sufixos de uma base de dados

        Args
        -----
            document: dict( { text, tag } )
        
        Returns
        -----
            baseCleaning: list [(text:string, tag:string)], Lista das palavras do documento e sua Tag
        """

        baseCleaning = []
        for (text, tag) in document:
            text = re.sub(r'[^\w\s$]|http\S+','', text).lower()
            withStemming = [
                str(self.stemmer.stem(p))
                for p in text.split()
                if p not in self.stopWords
            ]
            baseCleaning.append((withStemming, tag))
        
        return baseCleaning
    
    def findUniqueWords(self, baseCleaning: list):
        """
        Preenche a uniqueWords da ClassifierModel com uma lista de palavras únicas da base de dados
        
        Args
        -----
            baseCleaning: list [(text:string, tag:string)], Lista das palavras do documento e sua Tag
        """

        allWords = []
        for (words, tag) in baseCleaning:
            allWords.extend(words)
        
        """
        FreqDist: list [string], Registra o número de vezes que cada resultado de um experimento ocorreu
        """
        
        frequency = FreqDist(allWords)
        keys = frequency.keys()
        self.classifierModel.uniqueWords = keys
    
    def extractWords(self, document: dict) -> dict:
        """
        Criar mapeamento boleano da Existencia das palavras

        Args
        -----
            document: dict( { text, tag } )
        
        Returns
        -----
            characteristics: dict [string: bool], Mapeamento das UniqueWords encontradas no texto
        """
        
        characteristics = {}
        for words in self.classifierModel.uniqueWords:
            characteristics['%s' % words] = (words in document)

        return characteristics
