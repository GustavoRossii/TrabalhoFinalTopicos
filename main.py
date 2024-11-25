import pandas as pd
from processar_csv import ProcessarCSV
from treinar_modelo import ModeloML
from analise_dados import AnalisarDados
from flask import Flask, render_template, request, url_for, redirect, session, send_from_directory, flash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def csv_exists():
    return 'csv_path' in session and os.path.exists(session['csv_path'])

def handle_missing_csv():
    flash('Por favor, faça o upload do arquivo CSV antes de acessar a página de treinamento.', 'warning')
    return redirect(url_for('upload'))

@app.route('/menu')
def menu():
    return render_template('menu.html', csv_exists=csv_exists())

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
        try:
            path_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename)
            arquivo.save(path_arquivo)

            processador_CSV = ProcessarCSV(path_arquivo)
            df = processador_CSV.ler_csv()
            session['csv_path'] = path_arquivo

            flash('Arquivo CSV carregado com sucesso!', 'success')
            return render_template('upload.html', df=df, message='Arquivo processado com sucesso!')
        except Exception as e:
            flash(f'Erro ao processar arquivo: {e}', 'error')
            return render_template('upload.html', message='Erro ao processar arquivo: {}'.format(e))

@app.route('/treinar', methods=['GET', 'POST'])
def treinar_route():
    if not csv_exists():
        return handle_missing_csv()

    if request.method == 'GET':
        return render_template('treinar.html')

    path_arquivo = session['csv_path']
    processador_CSV = ProcessarCSV(path_arquivo)
    df = processador_CSV.ler_csv()

    modelo = ModeloML(df)
    modelo.treinar_modelo(df, df['Screen On Time (hours/day)'])

    flash('Modelo treinado com sucesso!', 'success')
    return render_template('treinar.html', message='Modelo treinado com sucesso!')

@app.route("/prever", methods=['GET', 'POST'])
def prever():
    if request.method == 'GET':
        return render_template('prever.html')

    if 'csv_path' not in session:
        return redirect(url_for('menu'))

    modelo = request.form['modelo']
    sistema_operacional = request.form['sistema_operacional']
    tempo_app = int(request.form['uso_app'])
    tempo_tela = int(request.form['tempo_tela'])
    drenagem_bateria = int(request.form['drenagem_bateria'])
    num_apps = int(request.form['num_apps'])
    dados_usados = int(request.form['dados_usados'])
    idade = int(request.form['idade'])
    genero = request.form['genero']

    dados = {
        'Device Model': [modelo],
        'Operating System': [sistema_operacional],
        'App usage(min/day)': [tempo_app],
        'Screen On Time (/day)': [tempo_tela],
        'Battery Drain (mAh/day)': [drenagem_bateria],
        'Number of Apps Installed': [num_apps],
        'Data Usage (MB/day)': [dados_usados],
        'Age': [idade],
        'Gender' : [genero]
    }

    df = pd.DataFrame(dados)

    modelo_ml = ModeloML(df)
    previsao = modelo_ml.prever_modelo(df)

    return render_template('treinar.html', previsao=previsao)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route("/analisar", methods=['GET', 'POST'])
def analisar():
    print("Rota /analisar chamada")
    if request.method == 'GET':
        print("Método GET")
        return render_template('analise.html')

    if request.method == 'POST':
        print("Método POST")
        if 'csv_path' not in session:
            print("csv_path não encontrado na sessão")
            return redirect(url_for('menu'))

        path_arquivo = session['csv_path']
        print(f"Path do arquivo CSV: {path_arquivo}")
        processador_CSV = ProcessarCSV(path_arquivo)
        df = processador_CSV.ler_csv()
        print("DataFrame carregado:\n", df.head())

        analisador = AnalisarDados(df)
        path_figures = analisador.plotar_graficos()
        print(f"Paths dos gráficos: {path_figures}")

        return render_template('analise.html', path_figures=path_figures)

if __name__ == '__main__':
    app.run(debug=True)
