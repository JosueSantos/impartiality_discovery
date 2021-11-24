# coding: utf-8

import nltk
from nltk import sent_tokenize
from nltk import word_tokenize

from sentistrength import PySentiStr


class PySentiStrength():
    """
    Interface de relacionamento do usuário com a ferramenta SentiStrength
    """
    
    pySentiStr = PySentiStr()

    def __init__(self) -> None:
        """
        Realiza o Setup da ferramenta SentiStrength
        """
        
        self.pySentiStr.setSentiStrengthPath('files/sentiStrength/SentiStrength.jar')
        self.pySentiStr.setSentiStrengthLanguageFolderPath('files/sentiStrength/SentStrength_Data/')

        nltk.download('punkt')
    
    def getScore(self, doc: str) -> dict:
        """
        Realiza a análise de um documento
    
        Args
        -----
            doc: string, Texto a ser analisado
            
        Returns
        -----
            dict, Resultado da análise:
            {
                'positive': int,
                'negative': int,
                'neutral': int,
                'balance': str,
            }
        """
        
        result = self.pySentiStr.getSentiment(doc, score='trinary')
        positive, negative, neutral = list(result[0])

        sents = sent_tokenize(doc)
        length = len(sents)
        words = word_tokenize(doc)
        word_neutral = [
            "conforme",
            "segundo",
            "disse",
            "declarou", 
            "acordo",
            "diz", 
            "afirma",
            "argumenta",
            "enumera", 
            "explica", 
            "apontou",
            "pesquisa",
            "relatou",
            "relatório",
            "afirmou",
            "aponta",
            "informou", 
            "ressaltou",
            "escreveu",
            "ibope",
            "tse",
            "eleitoral",
            "agenda",
            "anunciou",
            "destacou",
            "ressalta",
            "frisou",
            "mencionou",
            "comenta",
            "informaram",
            "decidiu",
            "agenda",
            "determinou",
            "concluiu"
        ]
        words = list(filter(lambda word: word.lower() in word_neutral, words))
        count_neutral_words = len(words)

        balance = self.scoreClassifier(positive, negative, length, count_neutral_words)
        
        print(balance + ' - length: ' + str(length) + ' count_neutral_words: '+ str(count_neutral_words))
        
        return {
            'positive': positive,
            'negative': negative,
            'neutral': neutral,
            'balance': balance,
            'length': length,
            'count_neutral_words': count_neutral_words,
        }
    
    def scoreClassifier(self, positive: int, negative: int, length: int, count_neutral_words: int) -> str:
        """
        Para definir o equilibrio verifica se não há valores além do limite +2 | -2
    
        Args
        -----
            positive: int, Medida Positiva da analise
            negative: int, Medida Negativa da analise
            
        Returns
        -----
            str, Resultado do balanço: impartial / partial
        """

        porcNeutral = count_neutral_words / length
        if (porcNeutral > 0.6):
            return "impartial"
        elif (positive < 3 and negative > -3):
            return "impartial"
        else:
            return "partial"
