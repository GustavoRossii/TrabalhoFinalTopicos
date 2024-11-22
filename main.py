from processar_csv import ProcessarCSV
from treinar_modelo import ModeloML
from analise_dados import AnalisarDados
from flask import Flask, render_template, request, url_for, redirect, session
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

@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if request.method == 'GET':
        return render_template('upload.html')

    if 'arquivoCSV' not in request.files:
        return redirect(url_for('upload'))

    arquivo = request.files['arquivoCSV']

    if arquivo.filename == '':

        return redirect(url_for('upload'))

    if arquivo:
        path_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename)
        arquivo.save(path_arquivo)

        processador_CSV = ProcessarCSV(path_arquivo)
        df = processador_CSV.ler_csv()
        session['csv_path'] = path_arquivo

        return render_template('upload.html', df=df)

@app.route('/treinar', methods=['GET', 'POST'])
def treinar():
    if  request.method == 'GET':
        return render_template('treinar.html')

    if 'csv_path' not in session:
        return redirect(url_for('treinar'))


    path_arquivo = session['csv_path']
    processador_CSV = ProcessarCSV(path_arquivo)
    df = processador_CSV.ler_csv()

    modelo = ModeloML(df)
    modelo.treinar_modelo(df)

    return 'Modelo treinado com sucesso!'


@app.route("/analisar", methods=['GET', 'POST'])
def analisar():

    if request.method == 'GET':
        return render_template('analise.html')


    if 'csv_path' not in session:
        return redirect(url_for('menu'))

    path_arquivo = session['csv_path']
    processador_CSV = ProcessarCSV(path_arquivo)
    df = processador_CSV.ler_csv()

    analisador = AnalisarDados(df)
    path_figuras = analisador.plotar_graficos(df)

    return render_template('analise.html', path_figuras=path_figuras)

if __name__ == '__main__':
    app.run(debug=True)
