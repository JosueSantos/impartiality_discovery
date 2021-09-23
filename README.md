# Impartiality Discovery
### Autor: Josue.Santos

## Tecnologias
- Python 3.8.5
- Biblioteca Scrapy [ pip install scrapy ]
- Biblioteca NLTK [ pip install nltk ]

## Objetivo
* Utilizar o processamento de linguagem natural para classificação automática de textos

  * Mineração de Textos utilizando a Classificação Supervisionada

A **Mineração de Textos** é uma das subáreas da Inteligência Artificial que tem como uma de suas metas básicas a localização de padrões em textos. Padrões utilizados para uma classificação em rótulos.

A **classificação** é a tarefa de escolher o rótulo de classe correto para uma determinada entrada. Em tarefas básicas de classificação, cada entrada é considerada isoladamente de todas as outras entradas, e o conjunto de rótulos é definido com antecedência.

Um classificador é denominado **supervisionado** se for construído com base em treinamento contendo o rótulo correto para cada entrada.

## Coleta de Dados

Executando o **scriptUpdateURLs.py**, ele irá executar os cralwers necessários para a captura das url's das notícias dos sites Diário do Nordeste, G1 e O Povo, removendo as url's duplicadas e salvando o progresso nos arquivos CSV no caminho:

 - **files/extractor/diarioDoNordeste/urls_dn.csv**
 - **files/extractor/g1Ceara/urls_g1.csv**
 - **files/extractor/oPovo/urls_op.csv**

Esta etapa deve se repetir diariamente até ser capturada uma grande quantidade de url's

Após a criação destas listas de URL's o script **scriptExtractor.py** deve ser executado para iniciar a coleta dos dados.

Na organização do projeto, o serviço *ExtractorService* realiza o papel de interface entre o usuário e o Scrapy.

## Scrapy

O Scrapy é uma biblioteca que possui funcionalidades de um Web crawler.

Web crawler é um programa que recolhe informações na internet de forma sistematizada através do protocolo padrão da web (http/https).

## ExtractorService.extractData()

O extractData() é necessário ser executado diversas vezes até que uma quantidade satisfatória de dados seja capturada.

Por conta disto, os dados capturados são salvos no formato CSV, no caminho registrado em **Base.CRAWLER_PATH**. Todos os arquivos CSV são lidos e preenchida uma lista de URLs vasculhadas.

Esta lista é comparada com as URLs disponíveis em **Base.URLS_(DN/G1/OP)** (**files/extractor/urls_(dn/g1/op).csv**), e será realizado a raspagem de dados apenas das URLs que ainda não foram capturadas. Neste processo é evitado o retrabalho.

Logo após, os Spiders são executados, onde vasculham cada uma das URLs disponíveis e captura os dados dos seus respectivos sites.

Ao término da raspagem deve ser executado o **scriptBuildData.py** que  coleta os arquivos CSV obtidos pelos crawlers e recolhe as informações. Realiza a analise da SentiStrength para cada uma das entradas.

Com o método **PySentiStrength.scoreClassifier()** classifica as notícias como imparciais se estiverem em equilibrio entre os pesos positivos e negativos obtidos pelo SentiStrength

Gerando como resultado de três arquivos CSV:

 - *Base.BASE*
 - *Base.BASE_IMPARTIAL*
 - *Base.BASE_PARTIAL*

Também realiza a limpeza da base removendo arquivos vazios.

Após a criação destes arquivos ocorre a partição da Base em treino e teste

Gerando 2 arquivos:

 - *Base.TRAINING*
 - *Base.TEST*

## Rotulagem dos Dados

Para uma classificação supervisionada é necessário que os dados estejam rotulados.

Neste ponto existirá os arquivos:

- **files/classifier/base.csv** : Com a base completa armazenada
- **files/classifier/base_training.csv** : Cerca de 30% da base rotulada total, utilizado para o treinamento do modelo
- **files/classifier/base_test.csv** : Com os outros 70% da base rotulada, para a validação do modelo

Estes dados rotulados serão utilizados para fazer com que o algoritmo aprenda os padrões para categoriza-los. Esta divisão da base em duas (treinamento e teste), acontece porque precisamos avaliar o algoritmo quanto à sua assertividade e uma das bases será utilizada para essa função.

## Preparação para o Modelo

A biblioteca NLTK (Natural Language Toolkit) já vem com funções preparadas que auxiliam a deixar a codificação mais prática e tira a necessidade de fazer os cálculos manualmente.

Para utilizar o NLTK, utilize o comando prompt de comando:
```
pip install nltk
```

O script **scriptClassifier.py** deve ser executado para iniciar o modelo.

### RLSP
Ao iniciar a execução do algoritimo **scriptClassifier.py** será realizado o download ou update do pacote RSLP (Removedor de Sufixos da Língua Portuguesa) que é um conjunto de funções de tratamento de textos específico para a nossa língua portuguesa (pt-br).

## ClassifierController
Foi criado um ClassifierModel para armazenar o modelo gerado, um controlador para todas as ações do classificador: ClassifierController. E um serviço para servir de interface entre o usuário final e o controlador: ClassifierService.

``` python
classifierService = ClassifierService()
```

Ao carregar o ClassifierService, ele se encarrega de chamar todas as funções necessarias para a preparação do modelo.

``` python
self.classifierController.buildBase( getBase(Base.TRAINING) )
self.classifierController.train()

self.classifierController.classifierModel.saveModel()
```

## ClassifierController.buildBase()
Esta função realiza o pré-processamento completo da Base de Dados. Utilizando alguns métodos:

- ### ClassifierController.baseCleaning()
*Stopword* são palavras que possuem significado sintático dentro da sentença, porém não trazem informações relevantes. As *stopwords* possuem uma grande frequência em qualquer idioma e por isso devem ser removidas do texto da base de dados. Caso contrário, o algoritmo poderia dar importância para palavras como: “e”, “ou”, “para”, etc. Isso certamente atrapalharia análise.

``` python
self.stopwords = set(stopwords.words('portuguese'))
self.stopwords.discard('não')
```

É utilizado a função SET não permite elementos repetidos e também compreensão de lista. E configurado o idioma das stopwords, no caso português. E removido desta lista a sentença 'NÃO' pelo seu impacto no sentido de qualquer frase

Além das *stopwords* também serão removidas as pontuações com excessão do cifrão monetário ($).
Também serão removidos os links, visto que não trazem sentindo relevante para a análise.

``` python
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
```

Após, será realizado o *stemming*, que é a técnica de retirar os prefixos e sufixos das palavras, deixando apenas seus radicais. Ex.: para Amor, Amado e Amável o radical é Am. Desta forma as 3 palavras serião tratadas como uma só, fazendo com que o algoritmo seja mais rápido e dinâmico.

- ### ClassifierController.findUniqueWords()
Este método busca todas as palavras únicas da base de dados, sem considerar seus rótulos, e preenche a *uniqueWords* da *ClassifierModel*.

- ### nltk.classify.apply_features()
O objetivo principal desta função é evitar a sobrecarga de memória envolvida no armazenamento de todos os conjuntos de recursos para cada token em uma base. Em vez disso, esses conjuntos de recursos são construídos lentamente, conforme necessário.

Um dos parametros da apply_features é a função extractWords(), esta função classifica as palavras como True, se estiverem dentro da nossa lista de palavras únicas, ou False se ela não está em nossa lista de palavras únicas.

## Pickle
Cada vez que fosse executado o algoritmo ainda seria necessário rodar todas as células novamente, para evitar este retrabalho existe uma biblioteca chamada pickle capaz de exportar estruturas de dados para um arquivo e importá-las em qualquer outra máquina.

O pickle permite a serialização de objetos, ou seja, os transforma em sequências de bytes. Armazenando toda informação necessária, consegue reconstruir objetos aplicando uma lógica interna.

Aproveitando este recurso temos o método *saveModel* e *getModelSaved* no *ClassifierModel* para o registro e leitura do modelo.

## Accuracy Metric
Para se analisar a precisão do modelo é necessário de uma duplicação do *ClassifierController* para realizar a *buildBase* da base de testes juntamente com a base de treinamento.

``` python
classifierController.buildBase( getBase(Base.TRAINING) )
classifierController.train()

classifierControllerTest = ClassifierController()
classifierControllerTest.buildBase( getBase(Base.TEST) )

accuracy = classifierController.accuracy(classifierControllerTest.base)
print("Acurácia do Modelo Gerado:")
print(accuracy)
```
Após o treinamento da base, o modelo pode ser medido sua Acurácia.

*O método **getBase** transformar os dados dos arquivos CSV em Listas para serem utilizadas do modelo.

## Matriz de Confusão
Com o modelo criado, pode ser gerado a matriz de confusão que é uma forma intuitiva de saber como o classificador está se comportando, ja que só a acurácia não é suficiente para determinar a precisão de uma algoritmo.

``` python
expected = []
predicted = []

for (phrase, tag) in classifierControllerTest.base:
    resultado = classifierController.classifierModel.classifier.classify(phrase)

    predicted.append(resultado)
    expected.append(tag)

matriz = ConfusionMatrix(expected, predicted)
print("Matriz de Confusão")
print(matriz)
```

## Utilizando o modelo
Para utilizar a categorização do modelo em um texto único:

``` python
text = 'Texto há ser analisado...'
tag = classifierService.classifySentence(text)
print(tag)
```

Para uma visualização mais detalhada da distribuição das porcentagens do modelo para aquela frase:

``` python
text = 'Texto há ser analisado...'
classifierService.distributionProbSentence(text)
```
