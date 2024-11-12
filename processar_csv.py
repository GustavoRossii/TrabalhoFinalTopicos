import pandas as pd

class ProcessarCSV:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo


    def ler_csv(self):
        return pd.read_csv(self.caminho_arquivo)