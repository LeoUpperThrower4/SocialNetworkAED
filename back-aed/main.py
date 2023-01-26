import matplotlib.pyplot as plt
from time import sleep
from app import app, db

plt.figure()

while True:
    command = input("Escreava um comando: (1) logar, (2) criar conta, (3) sair: ")
    if command == "3":
        database.dump_to_pkl()
        break
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
                command = input("Escreva um comando: (1) adicionar, (2) remover, (3) encontrar, (4) gerar grafo, (5) sair: ")
                if command == "5":
                    database.dump_to_pkl()
                    break
                elif command == "1":
                    email = input("Email: ")
                    user2 = db.getUser(email)
                    if not user2:
                        print("Usuário não encontrado")
                    else:
                        db.addConnection(user, user2)
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
                    searchResults = db.dumbSearch(searchKey, search)
                    print(searchResults)
                elif command == "4":
                    db.generateGraph(user)
                    plt.show()
                else:
                    print("Comando inválido")
