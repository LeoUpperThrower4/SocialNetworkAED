from flask import Flask, request, jsonify
from flask_cors import CORS
from socialNet import SimpleNet
import json

# app = Flask(__name__)
# CORS(app)
db = SimpleNet()

def signup(name, email, password, hasPrivateName, hasPrivateEmail, isCompany):
    tipo = 'person'
    if isCompany:
        tipo = 'company'

    response = db.createAccount(email, password, tipo, name, hasPrivateName, hasPrivateEmail)
    if response == 'ALREADY_SIGNED_UP':
        return "Usuário já Cadastrado", 401
    else:
        return "", 200

@app.route('/login', methods=['POST'])
def login():
    body = json.loads(request.data.decode())
    email = body['email']
    password = body['password']
    user = db.getUser(email)
    if not user:
        return "Invalid information", 400
    if user.value['password'] != password:
        return "Invalid information", 401
    userCopy = user.copy()
    return jsonify(userCopy), 200

@app.route('/relations', methods=['GET'])
def load_relations():
    userName = request.args.get('email')
    user = db.getUser(userName)
    response = db.getAllConnections(user)
    return jsonify({'relations': response}), 200

@app.route('/entities', methods=['GET'])
def load_entities():
    search = request.args.get('search')
    searchKey = request.args.get('searchKey')
    searchResults = db.dumbSearch(searchKey, search)
    return jsonify({'entities': searchResults}), 200
