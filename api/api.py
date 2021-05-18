import flask
from flask.json import jsonify
import json

def spaces_to_underline(s):
    return s.replace(" ","_")

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# salva o json em uma variavel
with open('dados.json','r') as f:
    data = json.load(f)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>O que eles andam fazendo?</h1>
<h3>Esta API retorna dados das atividades de alguns deputados.</h3>
<p>1. Retorna todas as propostas. - /api/v1/propostas/</p>
<p>2. Retorna todas as propostas filtradas por tipo de proposta - ex: /api/v1/propostas/tipo?Projeto_de_Lei </p>
<UL>2.1 Os tipos disponiveis são: Proposta_de_Lei e Proposta_de_Emenda_à_Constituição</UL>
<p>3. Retorna todas as propostas filtradas por autor desejado - ex: /api/v1/propostas/autor?Carla_Zambelli </p>'''

@app.route('/api/v1/propostas/', methods=['GET'])
def show_all_proposals():
    return jsonify(data["dados"])

@app.route('/api/v1/propostas/tipo/<type>', methods=['GET'])
def show_proposals_by_type(type):
    proposals_by_type = []
    for proposal in (data["dados"]):
        if (spaces_to_underline(proposal["descricaoTipo"]) == type):
            proposals_by_type.append(proposal)
    
    return jsonify(proposals_by_type)

@app.route('/api/v1/propostas/autor/<target_author>', methods=['GET'])
def show_proposals_by_author(target_author):
    proposals_by_author = []
    for proposal in (data["dados"]):
        for author in range(len(proposal["autores"])):
            if (spaces_to_underline(proposal["autores"][author]["nomeAutor"]) == target_author):
                proposals_by_author.append(proposal)
    
    return jsonify(proposals_by_author)

app.run()
