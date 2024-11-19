from sklearn.model_selection import train_test_split
import xgboost as xgb
import joblib


class ModeloML:
    def __init__(self, df):
        self.df = df

    def treinar_modelo(self, df, x, y):

        X_train, X_test, Y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        modelo = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')

        modelo.fit(X_train, Y_train)

        joblib.dump(modelo, 'modelo.pkl')

        return modelo
