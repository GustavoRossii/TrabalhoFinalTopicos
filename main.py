import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from processar_csv import ProcessarCSV
from treinar_modelo import treinar_modelo
from analise_dados import AnalisarDados

# Configuração da aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Garantir que o diretório de uploads exista
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# Funções auxiliares -> Verificar se o arquivo CSV foi carregado e existe
def csv_exists():
    return 'csv_path' in session and os.path.exists(session['csv_path'])


def handle_missing_csv():
    flash('Por favor, faça o upload do arquivo CSV antes de acessar a página de treinamento.', 'warning')
    return redirect(url_for('upload'))


# Rotas
@app.route('/')
def index():
    return redirect(url_for('menu'))

# Rota para a página de menu
@app.route('/menu')
def menu():
    return render_template('menu.html', csv_exists=csv_exists())

# Rota para upload de arquivos CSV
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Rota para upload de arquivos CSV."""
    if request.method == 'GET':
        return render_template('upload.html')

    arquivo = request.files.get('arquivoCSV')

    if not arquivo or arquivo.filename == '':
        flash('Nenhum arquivo selecionado. Por favor, faça o upload de um arquivo CSV.', 'error')
        return redirect(url_for('upload'))

    if not arquivo.filename.endswith('.csv'):
        flash('Formato inválido. Por favor, faça o upload de um arquivo CSV.', 'error')
        return redirect(url_for('upload'))

    try:
        path_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename)
        arquivo.save(path_arquivo)

        processador_CSV = ProcessarCSV(path_arquivo)
        df = processador_CSV.ler_csv()
        session['csv_path'] = path_arquivo

        flash('Arquivo CSV carregado com sucesso!', 'success')
        return render_template('upload.html', df=df)
    except Exception as e:
        flash(f'Erro ao processar o arquivo: {e}', 'error')
        return render_template('upload.html')

# Rota para treinamento do modelo
@app.route('/treinar', methods=['GET', 'POST'])
def treinar_route():
    if not csv_exists():
        return handle_missing_csv()

    if request.method == 'GET':
        return render_template('treinar.html')

    try:
        # Coletar dados do formulário
        form_data = {
            'Device Model': [request.form['modelo_dispositivo']],
            'App Usage Time (min/day)': [int(request.form['uso_apps'])],
            'Number of Apps Installed': [int(request.form['num_apps'])],
            'Data Usage (MB/day)': [int(request.form['uso_dados'])],
            'Age': [int(request.form['idade'])],
            'Operating System': [request.form['sistema_operacional']],
            'Battery Drain (mAh/day)': [int(request.form['drenagem_bateria'])],
            'Gender': [request.form['genero']]
        }

        path_arquivo = session['csv_path']
        processador_CSV = ProcessarCSV(path_arquivo)
        df = processador_CSV.ler_csv()

        modelo = treinar_modelo(df)
        df_previsao = pd.DataFrame(form_data)
        previsao = modelo.prever_modelo(df_previsao)

        flash('Modelo treinado e previsão realizada com sucesso!', 'success')
        return render_template('treinar.html', previsao=previsao[0])
    except Exception as e:
        flash(f'Erro ao treinar modelo: {e}', 'error')
        return redirect(url_for('treinar_route'))

# Rota para analise usando gráficos
@app.route('/analisar', methods=['GET', 'POST'])
def analisar():
    if request.method == 'GET':
        return render_template('analise.html')

    if not csv_exists():
        return redirect(url_for('menu'))

    try:
        path_arquivo = session['csv_path']
        processador_CSV = ProcessarCSV(path_arquivo)
        df = processador_CSV.ler_csv()

        analisador = AnalisarDados(df)
        path_figures = analisador.plotar_graficos()

        return render_template('analise.html', path_figures=path_figures)
    except Exception as e:
        flash(f'Erro ao analisar dados: {e}', 'error')
        return redirect(url_for('menu'))

# Rota para servir arquivos estáticos
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    app.run(debug=True)
