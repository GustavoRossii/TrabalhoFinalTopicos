import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

class ModeloML:
    def __init__(self, df):
        self.modelo = None
        self.df = df
        self.label_encoders = {}
        self.feature_names = None

    def treinar_modelo(self, x, y):
        # Remover colunas irrelevantes
        X = x.drop(columns=['User ID', 'Screen On Time (hours/day)'], axis=1)
        Y = y.astype(float)  # Converter para float

        # Aplicar Label Encoding
        for col in X.select_dtypes(include=['object']).columns:
            self.label_encoders[col] = LabelEncoder()
            X[col] = self.label_encoders[col].fit_transform(X[col])

        # Salvar os nomes das features
        self.feature_names = X.columns.tolist()

        # Dividir os dados em treino e teste
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        # Configurar e treinar o modelo (agora usando RandomForestRegressor)
        self.modelo = RandomForestRegressor(n_estimators=100, random_state=42)
        self.modelo.fit(X_train, Y_train)

        # Salvar o modelo treinado e as informações das features
        joblib.dump({
            'modelo': self.modelo,
            'label_encoders': self.label_encoders,
            'feature_names': self.feature_names
        }, 'modelo_info.pkl')

    def prever_modelo(self, x):
        if self.modelo is None:
            # Carregar o modelo e as informações das features
            info = joblib.load('modelo_info.pkl')
            self.modelo = info['modelo']
            self.label_encoders = info['label_encoders']
            self.feature_names = info['feature_names']

        # Preparar os dados de entrada
        x = x.reindex(columns=self.feature_names, fill_value=0)

        # Aplicar Label Encoding nas colunas categóricas
        for col, le in self.label_encoders.items():
            if col in x.columns:
                x[col] = le.transform(x[col])

        # Fazer a previsão
        previsao = self.modelo.predict(x)

        return previsao.round(2)  # Arredondar para 2 casas decimais