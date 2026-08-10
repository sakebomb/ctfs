from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/.git/<path:path>')
def serve_git(path):
    return send_from_directory('fakegit', path)

@app.route('/fakegit/<path:path>')
def serve_fakegit(path):
    return send_from_directory('fakegit', path)

@app.route('/.env')
def serve_env():
    return send_from_directory('.', '.env')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 