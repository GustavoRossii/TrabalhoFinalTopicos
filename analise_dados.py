import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

class AnalisarDados:

    def __init__(self, df):
        self.df = df


    def plotar_graficos(self, df):

        # sistema operacional -> bateria
        sns.swarmplot(x='Operating System', y='Battery Drain (mAh/day)', data=df)
        plt.title("Drenagem de bateria x Sistema operacional")
        plt.ylabel("Bateria gasta (mAh/dia)")
        plt.xlabel("Sistema operacional")
        grafico_SB = plt.gcf()
        plt.show()

        static_dir = 'static'
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
        file_path = os.path.join(static_dir, 'graficoSB.png')
        grafico_SB.savefig(file_path, format='png')

        return file_path