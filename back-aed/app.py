from socialNet import SimpleNet

db = SimpleNet()
relations = []
entities = []

def signup(name, email, password, hasPrivateName, hasPrivateEmail, isCompany):
    tipo = 'person'
    if isCompany:
        tipo = 'company'

    response = db.createAccount(email, password, tipo, name, hasPrivateName, hasPrivateEmail)
    if response == 'ALREADY_SIGNED_UP':
        return "Usuário já Cadastrado", 401
    else:
        return "", 200

def login(email, password):
    user = db.getUser(email)
    if not user:
        return "Invalid information", 400
    if user.value['password'] != password:
        return "Invalid information", 401
    userCopy = user.copy()
    return jsonify(userCopy), 200

def load_relations(email):
    user = db.getUser(email)
    self.relations = db.getAllConnections(user)

def load_entities():
    search = request.args.get('search')
    searchKey = request.args.get('searchKey')
    self.entities = db.dumbSearch(searchKey, search)
