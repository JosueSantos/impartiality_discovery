# coding: utf-8


from classifier.ClassifierService import ClassifierService


print("Read the README.md")

classifierService = ClassifierService()

text = 'O mercado internacional e a bolsa brasileira, a B3, sentiram a pressão que uma das maiores incorporadoras na China poderá causar nas cadeias globais caso não consiga quitar os débitos. Analistas comentam que o impacto sentido, de leve queda no início do dia, nas bolsas pelo mundo, foi apenas uma sinalização da crise que poderá vir, mesmo em patamar menor da observada em 2008, causado pela quebra do banco Lehman Brothers (Estados Unidos). No Brasil, a previsão é de aumento da pressão inflacionária e perdas para empresas de mineração.'

print(text)
print(classifierService.classifySentence(text))

print('---------------------')
classifierService.distributionProbSentence(text)
