from processar_csv import ProcessarCSV
from treinar_modelo import ModeloML
from flask import Flask, render_template, request, url_for, redirect
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/menu')
def menu():
    return render_template('menu.html')
@app.route('/')
def index():
    return redirect(url_for('menu'))

@app.route('/upload', methods=['POST'])
def upload():
    if 'arquivoCSV' not in request.files:
        return redirect(request.url)

    arquivo = request.files['arquivoCSV']

    if arquivo.filename == '':
        return redirect(request.url)

    if arquivo:
        path_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename)
        arquivo.save(path_arquivo)

        processador_CSV = ProcessarCSV(path_arquivo)
        df = processador_CSV.ler_csv()


        return df.head(5).to_html()

@app.route('/treinar', methods=['POST'])
def treinar():
    if 'arquivoCSV' not in request.files:
        return redirect(request.url)

    arquivo = request.files['arquivoCSV']

    if arquivo.filename == '':
        return redirect(request.url)

    if arquivo:
        path_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename)
        arquivo.save(path_arquivo)

        processador_CSV = ProcessarCSV(path_arquivo)
        df = processador_CSV.ler_csv()

        modelo = ModeloML(df)
        modelo.treinar_modelo()

        return 'Modelo treinado com sucesso!'

if __name__ == '__main__':
    app.run(debug=True)
