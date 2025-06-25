from flask import Flask, send_from_directory
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return """
    <h2>Servidor de Datos EURUSD 📊</h2>
    <ul>
        <li><a href='/eurusd.csv'>eurusd.csv</a></li>
        <li><a href='/vix.csv'>vix.csv</a></li>
        <li><a href='/dxy.csv'>dxy.csv</a></li>
    </ul>
    """

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory(BASE_DIR, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
