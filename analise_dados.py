import os
import matplotlib.pyplot as plt
import seaborn as sns

class AnalisarDados:

    def __init__(self, df):
        self.df = df

    def plotar_graficos(self):
        try:
            print("gerar gráfico")
            sns.swarmplot(x='Operating System', y='Battery Drain (mAh/day)', data=self.df)
            plt.title("Drenagem de bateria x Sistema operacional")
            plt.xlabel("Sistema operacional")
            plt.ylabel("Drenagem de bateria (mAh/dia)")
            grafico_SB = plt.gcf()


            static_dir = os.path.join('static', 'graficos')
            print(f"diretório para salvar grafico: {static_dir}")
            os.makedirs(static_dir, exist_ok=True)


            file_path = os.path.join(static_dir, 'graficoSB.png')
            print(f"salvando o grafico em: {file_path}")
            grafico_SB.savefig(file_path, format='png')
            plt.close()

            print("grafico gerado com sucesso!")
            return 'graficos/graficoSB.png'
        except Exception as e:
            print(f"Erro ao gerar o gráfico: {e}")
            return None

