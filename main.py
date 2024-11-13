from processar_csv import ProcessarCSV
from treinar_modelo import ModeloML
from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

@app.route('/menu')
def menu():
    return render_template('menu.html')
@app.route('/')
def index():
    return redirect(url_for('menu'))

@app.route('/upload', methods=['POST'])
def upload():
    if 'arquivoCSV' not in request.files:
        return 'Arquivo não encontrado'

    arquivo = request.files['arquivoCSV']

    if arquivo.filename == '':
        return 'Arquivo não encontrado'

    if arquivo and arquivo.filename.endswith('.csv'):
        arquivo.save(os.path.join('uploads', arquivo.filename))
        return 'Arquivo salvo com sucesso'



if __name__ == '__main__':
    app.run(debug=True)
