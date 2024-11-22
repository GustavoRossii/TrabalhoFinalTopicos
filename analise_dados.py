import os
import matplotlib.pyplot as plt
import seaborn as sns

class AnalisarDados:
    def __init__(self, df):
        self.df = df

    def plotar_graficos(self):
        try:
            # Check if DataFrame is loaded correctly
            print("DataFrame head:\n", self.df.head())

            # Diretório para salvar os gráficos
            static_dir = os.path.join('static', 'graficos')
            os.makedirs(static_dir, exist_ok=True)
            print(f"Diretório para salvar os gráficos: {static_dir}")

            # Lista para armazenar os caminhos dos gráficos
            graficos_paths = []

            # Gerar primeiro gráfico
            print("Iniciando a geração do gráfico 1...")
            sns.swarmplot(x='Operating System', y='Battery Drain (mAh/day)', data=self.df)
            plt.title("Drenagem de bateria x Sistema operacional")
            plt.xlabel("Sistema operacional")
            plt.ylabel("Drenagem de bateria (mAh/dia)")
            file_path1 = os.path.join(static_dir, 'grafico1.png')
            plt.savefig(file_path1, format='png')
            plt.close()
            print(f"Gráfico 1 salvo em: {file_path1}")
            graficos_paths.append('graficos/grafico1.png')

            # Verifique se a coluna 'App usage (min/day)' existe no DataFrame
            if 'App usage (min/day)' in self.df.columns:
                # Gerar segundo gráfico
                print("Iniciando a geração do gráfico 2...")
                sns.boxplot(x='Operating System', y='App usage (min/day)', data=self.df)
                plt.title("Uso de aplicativos x Sistema operacional")
                plt.xlabel("Sistema operacional")
                plt.ylabel("Uso de aplicativos (min/dia)")
                file_path2 = os.path.join(static_dir, 'grafico2.png')
                plt.savefig(file_path2, format='png')
                plt.close()
                print(f"Gráfico 2 salvo em: {file_path2}")
                graficos_paths.append('graficos/grafico2.png')
            else:
                print("Coluna 'App usage (min/day)' não encontrada no DataFrame")

            # Gerar terceiro gráfico
            print("Iniciando a geração do gráfico 3...")
            sns.histplot(self.df['Age'], kde=True)
            plt.title("Distribuição de Idade")
            plt.xlabel("Idade")
            plt.ylabel("Frequência")
            file_path3 = os.path.join(static_dir, 'grafico3.png')
            plt.savefig(file_path3, format='png')
            plt.close()
            print(f"Gráfico 3 salvo em: {file_path3}")
            graficos_paths.append('graficos/grafico3.png')

            return graficos_paths
        except Exception as e:
            print(f"Erro ao gerar os gráficos: {e}")
            return None