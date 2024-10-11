from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    login_url = data.get('login_url') 
    home_url = data.get('home_url') 

    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = session.get(login_url, headers=headers)
    print("HTML Response:", response.text) 

    soup = BeautifulSoup(response.text, 'html.parser')
    logintoken_input = soup.find('input', {'name': 'logintoken'})

    if logintoken_input is None:
        return jsonify({'status': 'error', 'message': 'Token de connexion non trouvé'}), 500

    logintoken = logintoken_input.get('value')

    login_data = {
        'username': username,
        'password': password,
        'logintoken': logintoken 
    }

    response = session.post(login_url, data=login_data, headers=headers, allow_redirects=True)

    if response.url == home_url:
        home_response = session.get(home_url, headers=headers)
        home_soup = BeautifulSoup(home_response.text, 'html.parser')

        data_extracted = {
            'span': [element.get_text(strip=True) for element in home_soup.find_all('span')]
        }

        return jsonify({'status': 'success', 'message': 'Connexion réussie', 'data': data_extracted})
    else:
        return jsonify({'status': 'failure', 'message': 'Échec de la connexion'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
