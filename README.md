# TrabalhoFinalTopicos
Introdução
Este projeto é uma aplicação web para carregar, processar, analisar e realizar
previsões com base em dados provenientes de um arquivo CSV. Ele utiliza técnicas de
Machine Learning para treinar modelos preditivos e realizar análises exploratórias com
visualizações gráficas. A aplicação é construída em Flask e utiliza bibliotecas como
XGBoost, Pandas, Matplotlib e Seaborn.
Estrutura do Projeto
Diretórios e Arquivos
• main.py: Controla a aplicação web e define as rotas para interação com o
usuário.
• processar_csv.py: Responsável por processar e carregar o arquivo CSV.
• treinar_modelo.py: Contém a lógica de treinamento e previsão do modelo de
Machine Learning.
• analise_dados.py: Realiza análise exploratória dos dados e gera gráficos.
• templates/: Contém os arquivos HTML usados no front-end.
• static/: Diretório para arquivos estáticos, incluindo gráficos gerados e
arquivos CSS.
Dependências
As principais bibliotecas utilizadas no projeto são:
• Flask: Framework web para Python.
• Pandas: Manipulação de dados.
• Scikit-learn: Funções auxiliares para particionamento de dados.
• XGBoost: Modelo de Machine Learning usado para classificação.
• Joblib: Persistência do modelo treinado.
• Matplotlib e Seaborn: Visualização de dados.
Instale as dependências executando:
pip install -r requirements.txt
Subir o Servidor
Inicie o servidor Flask:
python main.py
A aplicação estará acessível no navegador em http://127.0.0.1:5000.
Fluxo de Uso
Carregar Arquivo CSV
• Acesse a rota /upload para carregar um arquivo CSV.
• O arquivo será processado e armazenado em session['csv_path'].
Treinar o Modelo
• Acesse a rota /treinar após carregar o CSV.
• O modelo será treinado utilizando os dados fornecidos e salvo como
modelo.pkl.
Realizar Previsões
• Acesse a rota /prever para submeter novos dados ao modelo.
• O modelo carregará modelo.pkl e retornará as previsões baseadas nos dados
fornecidos.
Analisar os Dados
• Acesse a rota /analisar para visualizar gráficos que ajudam a entender os
dados carregados.
Descrição dos Arquivos
1. main.py
Controla as rotas da aplicação Flask e define o fluxo principal:
• Rotas principais:
o /menu: Página inicial com links para funcionalidades.
o /upload: Página para upload do arquivo CSV.
o /treinar: Treinamento do modelo.
o /prever: Realização de previsões com base no modelo treinado.
o /analisar: Exibição de gráficos exploratórios.
• Funções auxiliares:
o csv_exists: Verifica se um arquivo CSV foi carregado.
o handle_missing_csv: Garante que o arquivo CSV seja carregado antes
de acessar funcionalidades dependentes.
2. processar_csv.py
Classe ProcessarCSV:
• Atributos:
o caminho_arquivo: Caminho do arquivo CSV carregado.
• Métodos:
o ler_csv: Retorna um DataFrame com os dados do arquivo CSV.
3. treinar_modelo.py
Classe ModeloML:
• Atributos:
o modelo: Instância do modelo de Machine Learning.
o df: DataFrame com os dados carregados.
• Métodos:
o treinar_modelo(x, y): Treina um modelo XGBoost com os dados
fornecidos.
o prever_modelo(x): Realiza previsões com base no modelo treinado.
4. analise_dados.py
Classe AnalisarDados:
• Atributos:
df: DataFrame com os dados carregados.
• Métodos:
plotar_graficos: Gera gráficos exploratórios e os salva no diretório
static/graficos.
Gráficos gerados:
• Drenagem de bateria x Sistema operacional: Mostra a relação entre o
consumo de bateria e o sistema operacional dos dispositivos.
• Distribuição de Idade: Representa a faixa etária dos usuários no conjunto de
dados.
Considerações Finais
• Validação de dados: Certifique-se de que o arquivo CSV possui colunas
compatíveis com as esperadas pelo modelo.
• Persistência do modelo: O modelo treinado é salvo como modelo.pkl e
carregado em operações de previsão.
• Extensibilidade: O sistema pode ser facilmente adaptado para suportar novos
tipos de análise ou modelos.
