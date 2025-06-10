import csv
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def carregar_dados():
    dados = {}
    with open("dados.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cpf = row["cpf"].strip()
            nome = row["nome"].strip()
            rastreio = row["rastreamento"].strip()
            dados[cpf] = {"nome": nome, "rastreio": rastreio}
    return dados

@app.route('/rastreio', methods=['POST'])
def rastrear():
    cpf = request.json.get("cpf")
    if not cpf:
        return jsonify({"erro": "CPF não enviado"}), 400

    dados = carregar_dados()
    resultado = dados.get(cpf)
    if resultado:
        return jsonify(resultado)
    return jsonify({"erro": "CPF não encontrado"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
