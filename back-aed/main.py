import matplotlib.pyplot as plt
from time import sleep
from app import db

plt.figure()

while True:
    command = input("Escreava um comando: (1) logar, (2) criar conta, (3) sair: ")
    if command == "3":
        db.saveGraph()
        break
    elif command == "2":
        name = input("Nome: ")
        email = input("Email: ")
        password = input("Senha: ")
        hasPrivateName = input("Nome privado? (s/n): ") == 's'
        isCompany = input("É uma empresa? (s/n): ") == 's'
        response = db.createAccount(email, password, 'company' if isCompany else 'person', name, hasPrivateName)
        if response == 'ALREADY_SIGNED_UP':
            print("Usuário já cadastrado")
        else:
            print("Criado com sucesso")
    elif command == "1":
        email = input("Email: ")
        password = input("Senha: ")
        user = db.getUser(email)
        if not user:
            print("Informações inválidas")
        elif user.value['password'] != password:
            print("Informações inválidas")
        else:
            print("Logado com sucesso")
            while True:
                command = input("Escreva um comando: (1) conectar, (2) desconectar, (3) encontrar, (4) gerar grafo, (9) sair: ")
                if command == "9":
                    db.saveGraph()
                    break
                elif command == "1":
                    email = input("Email: ")
                    user2 = db.getUser(email)
                    if not user2:
                        print("Usuário não encontrado")
                    else:
                        strText = 'Informe o "peso" da conexão: '
                        if (user2.value['type'] == 'company' or user.value['type'] == 'company'):
                            strText += '(cl)iente'
                        else:
                            strText += '(fa)mília, (co)nhecido, (a)migo'
                        weight = input(strText + ': ')
                        if weight == 'fa':
                            weight = 'family'
                            db.addFamily(user, user2)
                        elif weight == 'co':
                            db.addAcquaintance(user, user2)
                        elif weight == 'cl':
                            db.addClient(user, user2)
                        elif weight == 'a':
                            db.addFriendship(user, user2)
                        else:
                            print("Peso inválido")
                            continue
                        print("Adicionado com sucesso")
                elif command == "2":
                    email = input("Email: ")
                    user2 = db.getUser(email)
                    if not user2:
                        print("Usuário não encontrado")
                    else:
                        db.removeConnection(user, user2)
                        print("Removido com sucesso")
                elif command == "3":
                    search = input("Pesquisa: ")
                    searchKey = input("Chave de pesquisa: ")
                    searchResults = db.BFS(user, searchKey, search)
                    print(searchResults)
                elif command == "4":
                    db.saveGraph()
                    db.saveGraphImg(user)
                    plt.show()
                    db.saveGraphImg(user, levels=2)
                    plt.show()
                else:
                    print("Comando inválido")
