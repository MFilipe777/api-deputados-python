import flask
from flask import request
from flask.json import jsonify
import json

def spaces_to_underline(s):
    new_s = ''
    for i in s:
        if i == " ":
            new_s += "_"
        else:
            new_s += i
    return new_s

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Dados dos deputados
with open('dados.json','r') as f:
    data = json.load(f)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>O que eles andam fazendo?</h1>
<h3>Esta API retorna dados das atividades de alguns deputados.</h3>
<p>1. Retorna todas as propostas. - /api/v1/propostas/all</p>
<p>2. Retorna todas as propostas filtradas por tipo de proposta - ex: /api/v1/propostas/tipo?Projeto_de_Lei </p>
<UL>2.1 Os tipos disponiveis são: Proposta_de_Lei e Proposta_de_Emenda_à_Constituição</UL>
<p>3. Retorna todas as propostas filtradas por autor desejado - ex: /api/v1/propostas/autor?Carla_Zambelli </p>'''

@app.route('/api/v1/propostas/all', methods=['GET'])
def show_all_proposals():
    return jsonify(data["dados"])

@app.route('/api/v1/propostas/tipo', methods=['GET'])
def show_proposals_by_type():
    proposals_by_type = []
    for i in (data["dados"]):
        if (spaces_to_underline(i["descricaoTipo"]) in request.args):
            proposals_by_type.append(i)
    
    return jsonify(proposals_by_type)

@app.route('/api/v1/propostas/autor', methods=['GET'])
def show_proposals_by_author():
    proposals_by_author = []
    for i in (data["dados"]):
        for j in range(len(i["autores"])):
            if (spaces_to_underline(i["autores"][j]["nomeAutor"]) in request.args):
                proposals_by_author.append(i)
    
    return jsonify(proposals_by_author)

app.run()