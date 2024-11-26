import pandas as pd
from processar_csv import ProcessarCSV
from treinar_modelo import treinar_modelo
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

    if not arquivo.filename.endswith('.csv'):
        flash('Por favor, faça o upload de um arquivo CSV.', 'error')
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

    if request.method == 'POST':
        modelo_dispositivo = request.form['modelo_dispositivo']
        usoDeApps = int(request.form['app_usage'])
        num_apps = int(request.form['num_apps'])
        usoDeDados = int(request.form['data_usage'])
        idade = int(request.form['age'])

        path_arquivo = session['csv_path']
        processador_CSV = ProcessarCSV(path_arquivo)
        df = processador_CSV.ler_csv()

        modelo = treinar_modelo(df)
        modelo.treinar_modelo(df, df['Screen On Time (hours/day)'])

        # Prepare data for prediction
        dados = {
            'Device Model': [modelo_dispositivo],
            'App Usage Time (min/day)': [usoDeApps],
            'Number of Apps Installed': [num_apps],
            'Data Usage (MB/day)': [usoDeDados],
            'Age': [idade]
        }
        df_previsao = pd.DataFrame(dados)

        previsao = modelo.prever_modelo(df_previsao)

        flash('Modelo treinado com sucesso!', 'success')
        return render_template('treinar.html', previsao=previsao[0])

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route("/analisar", methods=['GET', 'POST'])
def analisar():
    if request.method == 'GET':
        return render_template('analise.html')

    if request.method == 'POST':
        if 'csv_path' not in session:
            return redirect(url_for('menu'))

        path_arquivo = session['csv_path']
        processador_CSV = ProcessarCSV(path_arquivo)
        df = processador_CSV.ler_csv()

        analisador = AnalisarDados(df)
        path_figures = analisador.plotar_graficos()

        return render_template('analise.html', path_figures=path_figures)

if __name__ == '__main__':
    app.run(debug=True)