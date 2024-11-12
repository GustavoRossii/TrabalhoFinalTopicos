import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class AnalisarDados:

    def __init__(self, df):
        self.df = df


    def analisar_dados(self):
        print(self.df.head())
        print(self.df.describe())
        print(self.df.info())
        print(self.df.isnull().sum())
        print(self.df.columns)


    def plotar_graficos(self):
        # Analisar os graficos a colocar
        pass