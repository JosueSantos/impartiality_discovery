# Impartiality Discovery
### Autor: Josue.Santos

## Tecnologias
- Python 3.8.5
- Biblioteca Scrapy [ pip install scrapy ]
- Biblioteca NLTK [ pip install nltk ]
- Biblioteca Pandas [ pip install pandas ]
- Ferramenta Jupyter Notebook [ pip install jupyter ]

## Objetivo
* Utilizar o processamento de linguagem natural para classificação automática de textos;

  * Mineração de Textos utilizando a Classificação Supervisionada;

A **Mineração de Textos** é uma das subáreas da Inteligência Artificial que tem como uma de suas metas básicas a localização de padrões em textos. Padrões utilizados para uma classificação em rótulos.

A **classificação** é a tarefa de escolher o rótulo de classe correto para uma determinada entrada. Em tarefas básicas de classificação, cada entrada é considerada isoladamente de todas as outras entradas, e o conjunto de rótulos é definido com antecedência.

Um classificador é denominado **supervisionado** se for construído com base em treinamento contendo o rótulo correto para cada entrada.

## Estrutura e Organização

Utilizando o conceito modular de organização, o projeto foi dividido em partes isoladas.

- **classifier** é responsável pela criação do modelo e armazena toda a lógica necessária para o tal.
- **extractor** é responsável pela captura dos dados, onde se realiza os crawlers;
- **files** onde são armazenados os arquivos extraidos e possui um utilitário com diversas funções de acesso a estes arquivos;
- **raiz** é o local dos scripts de acesso, para que com apenas uma execução toda a funcionalidade seja atendida;

## Ordem da Execução dos scripts

- scriptUpdateURLs.py
- scriptExtractor.py
- scriptBuildData.py
- scriptClassifier.py
- scriptPopulateAnalytics.py

## Coleta de Dados

Executando o **scriptUpdateURLs.py**, ele irá executar os cralwers necessários para a captura das url's das notícias dos sites Diário do Nordeste, G1 e O Povo, removendo as url's duplicadas e salvando o progresso nos arquivos CSV no caminho:

 - **files/extractor/diarioDoNordeste/urls_dn.csv**
 - **files/extractor/g1Ceara/urls_g1.csv**
 - **files/extractor/oPovo/urls_op.csv**

Esta etapa deve se repetir diariamente até ser capturada uma grande quantidade de url's.

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

## Ground Truth

Para a avaliação do modelo é necessário a comparação com uma base rotulada por um humano, para esta etapa do processo será criado um arquivo CSV manualmente na rota **files/ground_truth.csv** com a avaliação como "impartial/partial" seguido da url da notícia, este arquivo utilizará o delimitador de ponto e vírgula ";" utilizado nos outros arquivos do projeto. Observando que as notícias contidas na ground_truth deve ter sido capturada pelos crawlers para se possuir o conteúdo da notícia para a analise.

Esta analise manual obedece alguns critérios para a classificar como imparcial ou parcial:

Para ser considerada Parcial a notícia deve:
- Deduzir algo com a utilização dos termos: "deve ser", "poderá";
- Demostrar a emoção do jornalista;
- Exibir a opnião, trazendo algo além dos fatos;
- Ausência de relatos das partes envolvidas;

Será considerada Imparcial a notícia que não se enquadrar nos critérios de parcialidade.

## ScriptBuildData

Para o aprendizado de máquina é necessário uma grande quantidade de dados, visto que a rotulagem manual não é o suficiente para o treinamento e para o teste. A base Ground Truth será utilizada apenas para o teste, enquanto para o treinamento será utilizada uma base rotulada automaticamente a partir de algumas ferramentas.

Ao término da rotulagem manual deve ser executado o **scriptBuildData.py** que  coleta os arquivos CSV obtidos pelos crawlers e recolhe as informações e realiza a analise da SentiStrength para cada uma das entradas.

### SentiStrength

A ferramenta SentiStrength possui um dicionário léxico que atribui as palavras com emoções positivas valores entre 1 e 5 e a palavras com emoções negativas valores entre -1 e -5. Analisando a sentença que recebe, a divide em tokens e para cada palavra que transmite uma emoção é atribuída uma pontuação determinada. Após pontuar todas as palavras, a ferramenta retorna a pontuação máxima dos sentimentos negativos e a pontuação máxima dos sentimentos positivos.

### OpLexicon V3.0

Foi realizado um acréscimo ao dicionário léxico da ferramenta SentiStrength, com a mesclagem de sua base com a do OpLexicon, também conhecido como Sentiment Lexicon, que consiste de uma lista de palavras rotuladas como positivas e negativas. Este é um método léxico criado a partir de textos coletados em reviews de produtos em sites de compra.

### PySentiStrength.scoreClassifier()

Analisando as notícias rotuladas como imparcial foi percebido um padrão com a quantidade de palavras de citação em relação a quantidade de frases da notícia. Sendo que, se houvesse uma citação em pelo menos 60% das frases da noticia, esta teria maior chance de ser considerada imparcial.

As palavras de citação mapeadas foram:
- conforme
- segundo
- disse
- declarou
- acordo
- diz
- afirma
- argumenta
- enumera
- explica
- apontou
- pesquisa
- relatou
- relatório
- afirmou
- aponta
- informou
- ressaltou
- escreveu
- ibope
- tse
- eleitoral
- agenda
- anunciou
- destacou
- ressalta
- frisou
- mencionou
- comenta
- informaram
- decidiu
- agenda
- determinou
- concluiu

Com base nessa analise foi criado o método **PySentiStrength.scoreClassifier()** que classifica as notícias como imparciais se possuirem uma grande quantidade de palavras de citações ou estiverem próximas a neutralidade (+2 | -2) entre os pesos positivos e negativos obtidos pelo SentiStrength, levando em consideração que o limite dos valores das emoções é +5 e -5.

É executado a avaliação deste metodo para cada uma das notícias capturadas.

Gerando como resultado quatro arquivos CSV:

 - *Base.BASE*
 - *Base.BASE_IMPARTIAL*
 - *Base.BASE_PARTIAL*
 - *Base.BASE_GROUND_TRUTH*

Também realiza a limpeza da base removendo arquivos vazios.

Após a criação destes arquivos ocorre a partição da Base em treino e teste

Gerando 2 arquivos:

 - *Base.TRAINING*
 - *Base.TEST*

## Rotulagem dos Dados

Para uma classificação supervisionada é necessário que os dados estejam rotulados.

Neste ponto existirá os arquivos:

- **files/classifier/base.csv** : Com a base completa armazenada.
- **files/classifier/base_ground_truth.csv** : Com a base rotulada por humanos, para a validação do modelo.
- **files/classifier/base_training.csv** : Pode ser enviado por parametro a porcentagem que será entregue a base de treino, como utilizaremos os dados da base ground truth como teste esta base deve estar proximo de 100% da base total.
- **files/classifier/base_test.csv** : Recebera a sobra da porcentagem da base de treinamento, como a base ground truth será usada para o teste, esta deverá estar vazia.

Estes dados rotulados serão utilizados para fazer com que o algoritmo aprenda os padrões para categoriza-los. Esta divisão da base em duas (treinamento e teste), acontece porque precisamos avaliar o algoritmo quanto à sua assertividade e uma das bases será utilizada para essa função.

## Preparação para o Modelo

A biblioteca NLTK (Natural Language Toolkit) já vem com funções preparadas que auxiliam a deixar a codificação mais prática e tira a necessidade de fazer os cálculos manualmente.

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
```
Após o treinamento da base, o modelo pode ser medido sua Acurácia.

*O método **getBase** transformar os dados dos arquivos CSV em Listas para serem utilizadas do modelo.

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

## Após a geração do Modelo

Após a geração do Modelo baseado no Naive Bayes, execute o **scriptPopulateAnalytics**. Que irá avaliar novamente toda a base e criar um novo arquivo de treinamento. Este arquivo será utilizado em outra aplicação para aprimorar ainda mais a acurácia do modelo utilizando tecnicas de word embedding.

O sentido deste processo consiste em sempre melhorar a base de dados rotulada automaticamente, para que o próximo modelo gerado tenha uma acurácia ainda melhor.

A base rotulada pela ferramenta SentiStrength obteve uma acurácia de 57%, quando comparada com a base rotulada por humanos (base ground truth).

Já o modelo criado pelo NaiveBayes obteve uma acurácia de 73%, porém observando os rotulos separadamente, percebemos que a acertividade para nóticias imparciais foi de 84% quanto para nóticias parciais foi de apenas 33%. Necessitando de uma nova etapa na busca pelo modelo ideal.

Pode-se observar o processo utilizando as tecnicas de word embedding no notebook **ImpartialityDiscovery2021.ipynb**

Com o Word Embedding foi possível ter uma melhora no modelo. Com acurácia total de 77%, a acertividade de notícias imparciais foi para 84% e a das parciais subiu para 51%. Tornando assim um modelo muito mais confiável do que os anteriores.


