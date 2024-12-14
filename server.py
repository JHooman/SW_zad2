from flask import Flask, request, jsonify
import pytz
from datetime import datetime
import logging
import re
import json
import requests

# Konfiguracja logowania
logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Dane autora serwera
AUTHOR_NAME = "Aleksander Szczepocki"
PORT = 5000

# Informacje przy starcie serwera
logging.info(f"Server started by {AUTHOR_NAME} on port {PORT}")
print(f"Server started by {AUTHOR_NAME} on port {PORT}")
# Tworzenie aplikacji Flask
app = Flask(__name__)


def get_timezone(ip):
    response = requests.get(f"http://ip-api.com/json/{ip}")
    response = response.json()

    if 'timezone' in response:
        user_timezone = response['timezone']
    else:
        user_timezone = 'Europe/Warsaw'

    timezone = pytz.timezone(user_timezone)
    return timezone

@app.route('/')
def home():

    client_ip = request.remote_addr
    client_timezone = get_timezone(client_ip)
    utc_now = datetime.utcnow()
    local_time = utc_now.astimezone(client_timezone)
    formatted_time = local_time.strftime('%Y-%m-%d %H:%M:%S')

    return f"""
    <html>
        <head><title>Informacje o kliencie</title></head>
        <body>
            <h1>Informacje o Twoim połączeniu</h1>
            <p><strong>Twój adres IP:</strong> {client_ip}</p>
            <p><strong>Data i godzina w Twojej strefie czasowej:</strong> {formatted_time}</p>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)



