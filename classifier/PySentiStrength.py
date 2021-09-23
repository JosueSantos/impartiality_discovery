# coding: utf-8

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
        balance = self.scoreClassifier(positive, negative)
        
        print(balance + ' - positive: ' + str(positive) + ' negative: '+ str(negative)+' neutral: '+str(neutral))
        
        return {
            'positive': positive,
            'negative': negative,
            'neutral': neutral,
            'balance': balance,
        }
    
    def scoreClassifier(self, positive: int, negative: int) -> str:
        """
        Realiza o calculo para definir o equilibrio
    
        Args
        -----
            positive: int, Medida Positiva da analise
            negative: int, Medida Negativa da analise
            
        Returns
        -----
            str, Resultado do balanço: impartial / partial
        """

        if (positive < 3 and negative > -3):
            return "impartial"
        else:
            return "partial"
