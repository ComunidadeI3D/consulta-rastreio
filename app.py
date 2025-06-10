from flask import Flask, request, jsonify
from flask_cors import CORS
import csv

app = Flask(__name__)
CORS(app)

def carregar_dados():
    dados = {}
    with open("dados.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row = {k.strip().lower(): v.strip() for k, v in row.items()}  # padroniza colunas
            cpf = row.get("cpf")
            nome = row.get("nome")
            rastreio = row.get("rastreamento")
            if cpf and nome and rastreio:
                dados[cpf] = {"nome": nome, "rastreio": rastreio}
    return dados

@app.route("/rastreio", methods=["POST"])
def rastrear():
    try:
        cpf = request.json.get("cpf")
        if not cpf:
            return jsonify({"erro": "CPF não enviado"}), 400

        dados = carregar_dados()
        resultado = dados.get(cpf)
        if resultado:
            return jsonify(resultado)
        else:
            return jsonify({"erro": "CPF não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": f"Erro interno no servidor: {str(e)}"}), 500

@app.route("/")
def status():
    return "✅ Backend de rastreio está funcionando."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
