from flask import Flask, request, jsonify
from flask_cors import CORS  # <- ESTA LINHA FALTAVA
import csv

app = Flask(__name__)
CORS(app)  # <- Isso agora vai funcionar corretamente

def carregar_dados():
    dados = {}
    with open("dados.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for linha in reader:
            cpf, codigo = linha
            dados[cpf.strip()] = codigo.strip()
    return dados

@app.route('/rastreio', methods=['POST'])
def rastrear():
    cpf = request.json.get("cpf")
    if not cpf:
        return jsonify({"erro": "CPF não enviado"}), 400

    dados = carregar_dados()
    codigo = dados.get(cpf)
    if codigo:
        return jsonify({"rastreio": codigo})
    return jsonify({"erro": "CPF não encontrado"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
