from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route('/')
def home():
    with open('playbooks.json') as f:
        data = json.load(f)
    return render_template('index.html', playbooks=data)

@app.route('/api/playbooks')
def api_playbooks():
    with open('playbooks.json') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

