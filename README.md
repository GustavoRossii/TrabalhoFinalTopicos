# TrabalhoFinalTopicos
# Aplicação Web de Machine Learning para Análise de Dados CSV

## Descrição do Projeto

Este projeto é uma aplicação web desenvolvida em Flask para carregar, processar, analisar e realizar previsões com base em dados de um arquivo CSV. Utiliza técnicas de Machine Learning para treinar modelos preditivos e gerar análises exploratórias com visualizações gráficas.

## Estrutura do Projeto

### Diretórios e Arquivos

- `main.py`: Controla a aplicação web e define as rotas de interação
- `processar_csv.py`: Processamento e carregamento do arquivo CSV
- `treinar_modelo.py`: Lógica de treinamento e previsão do modelo de Machine Learning
- `analise_dados.py`: Análise exploratória e geração de gráficos
- `templates/`: Arquivos HTML do front-end
- `static/`: Arquivos estáticos (gráficos gerados, CSS)

## Dependências

As principais bibliotecas utilizadas no projeto:

- Flask: Framework web para Python
- Pandas: Manipulação de dados
- Scikit-learn: Funções auxiliares para particionamento de dados
- XGBoost: Modelo de Machine Learning para classificação
- Joblib: Persistência do modelo treinado
- Matplotlib e Seaborn: Visualização de dados

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual (opcional, mas recomendado)
3. Instale as dependências:

pip install -r requirements.txt

Executando a Aplicação

Inicie o servidor Flask

A aplicação estará disponível em: http://127.0.0.1:5000

Fluxo de Uso
1. Carregar Arquivo CSV

    Acesse /upload para carregar um arquivo CSV

2. Treinar o Modelo

    Acesse /treinar para treinar o modelo com os dados carregados

3. Realizar Previsões

    Acesse /prever para submeter novos dados e obter previsões

4. Analisar Dados

    Acesse /analisar para visualizar gráficos exploratórios

Gráficos Gerados

    Drenagem de bateria x Sistema operacional
    Distribuição de Idade

Considerações Importantes

    Valide se o arquivo CSV possui colunas compatíveis com o modelo
    O modelo treinado é salvo como modelo.pkl
    O sistema pode ser facilmente adaptado para novos tipos de análise

