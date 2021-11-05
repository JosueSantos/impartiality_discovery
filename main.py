# coding: utf-8

from classifier.ClassifierService import ClassifierService


print('Read the README.md')

classifierService = ClassifierService()

text = "Polícia apreende documentos do 'Mensalão do DEM' -- Brunelli é acusado de participar do esquema de distribuição de propina pelo governo do Distrito Federal, durante a gestão de José Roberto Arruda, escândalo que ficou conhecido por 'Mensalão do DEM', e que foi denunciado pelo delator do esquema, Durval Barbosa - que se filmou entregando dinheiro para o próprio Arruda e para uma série de parlamentares de Brasília. Nas filmagens de Durval, Brunelli reza depois de receber uma bolada de dinheiro - episódio que logo ganhou o nome de 'oração da propina'. Denúncias anônimas afirmavam que pastores da Igreja Tabernáculo do Evangelho de Jesus, localizada no Recanto das Emas, no Distrito Federal, estariam escondendo documentos sobre as pessoas investigadas pela Operação Hofini. 'Isso é ocultação de provas que interessam ao inquérito: conseguimos os mandados e fomos atrás', informa o delegado responsável pelas investigações, Henri Peres Lopes. Os mandados foram cumpridos na igreja e também na casa da advogada Marlucy de Senna Guimarães de Oliveira e na do pastor Valdir Niasato, ambas localizadas em Taguatinga, bairro nobre do Distrito Federal. Computadores, mídias eletrônicas, documentos contábeis e documentos relacionados aos investigados foram apreendidos por agentes da Delegacia de Repressão ao Crime Organizado de Brasília. Os documentos apreendidos comprovariam a lavagem de dinheiro por meio da Associação Monte das Oliveiras (AMO), informa o delegado Lopes. Brunelli fazia emendas orçamentárias para destinar recursos para a AMO que, por sua vez, deveria realizar projetos para a melhoria da qualidade de vida de idosos e crianças da região, mas não fazia nada, diz Lopes. Notas fiscais falsas justificavam grosseiramente o uso das verbas em eventos que nunca aconteceram, afirma Lopes. Após a etapa, concluída nesta segunda-feira, da Operação Hofini II, a presidente da AMO, Maria Soares de Almeida, e a tesoureira da associação, Maria das Mercês de Souza, foram indiciadas, além da advogada Marlucy e o pastor Valdir Niasato. O delegado afirma ainda que nenhuma prisão foi efetuada, mas a hipótese não pode ser descartada, 'uma vez que as investigações continuam, com o objetivo de identificar e tomar as devidas medidas, com os culpados e envolvidos no caso', afirma Lopes."

print(text)
print("\n\n")
print(classifierService.classifySentence(text))

print('---------------------')
classifierService.distributionProbSentence(text)
