# app.py

from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Use uma variável de ambiente para a chave da API
API_KEY = os.getenv('OPENWEATHER_API_KEY', 'sua chave aqui')  # Substitua pela sua chave da API OpenWeatherMap

@app.route('/')
def home():
    """Renderiza a página inicial do aplicativo."""
    return render_template('index.html')

@app.route('/clima', methods=['POST'])
def clima():
    """Obtém as informações do clima para a cidade fornecida pelo usuário.

    Retorna:
        dict: Um dicionário com as informações do clima.
    """
    cidade = request.form['cidade']
    url = f'http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric'
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        clima_info = {
            'cidade': dados['name'],
            'temperatura': dados['main']['temp'],
            'descricao': dados['weather'][0]['description'],
            'umidade': dados['main']['humidity']
        }
        return render_template('resultado.html', clima=clima_info)
    elif resposta.status_code == 404:
        return render_template('erro.html', mensagem='Cidade não encontrada!')
    elif resposta.status_code == 401:
        return render_template('erro.html', mensagem='Chave da API inválida!')
    else:
        return render_template('erro.html', mensagem='Erro ao acessar a API.')

if __name__ == '__main__':
    app.run(debug=True)