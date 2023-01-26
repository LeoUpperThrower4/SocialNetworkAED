import pickle
from graphClass import Graph
import matplotlib.pyplot as plt
import networkx as nx
import copy
from matplotlib.lines import Line2D

class SimpleNet:
    def __init__(self):
        """
        This is a SimpleNet class
        It is an interface between the windows and the graph
        """
        self.G = None

    def fromPkl(self):
        """
        Load graph from pickle
        """
        try:
            # Open the file in binary mode
            with open('out/graph.pkl', 'rb') as file:
                # Call load method to deserialize
                self.G = pickle.load(file)
        except:
            self.G = Graph()
            self.saveGraph()

    def saveGraph(self):
     # Open a file and use dump()
        with open('out/graph.pkl', 'wb') as file:
            pickle.dump(self.G, file)  # A new file will be created

    def getUsers(self):
        """
        Return network users / graph vertices
        """
        return self.G.getVertices()

    def getUser(self, id):
        """
        Return vertex instance given the id (key)
        """
        if self.G == None:
            self.fromPkl()

        return self.G.getVertex(id)       

    def createAccount(self, email, password, tipo, name, hasPrivateName):
        """
        Create account / add vertex to graph
        """
        if self.getUser(email) != None:
            return 'ALREADY_SIGNED_UP'

        # Poderiamos adicionar outras informações aqui. Deixamos só uma pra exemplificar
        privateList = []
        if hasPrivateName:
            privateList.append("name")

        self.G.addVertex(email, 
         {"email": email, "name": name,  "password": password,
            "private": privateList,
            "type": tipo})
        self.saveGraph()    

    def BFS(self, user, key, value):
        """
        Perform BFS to find user[key] = value
        """
        if key == "user":
            matches = self.G.BFS(
                user, True, lambda v: value in v.key)
        else:
            matches = self.G.BFS(user, True, lambda v: v.value['private'] and value in v.value[key])

        return matches

    def getConnection(self, user1, user2):
        """
        Get relatioship between two users
        """
        return self.G.getEdgeWeight(user1.key, user2.key)

    def addFriendship(self, user1, user2):
        """
        Add edge between two users with weight = friend
        """
        self.G.addEdge(user1.key, user2.key, weight="friend")
        self.G.addEdge(user2.key, user1.key, weight="friend")
        self.saveGraph()

    def addAcquaintance(self, user1, user2):
        """
        Add edge between two users with weight = acquaintance
        """
        self.G.addEdge(user1.key, user2.key, weight="acquaintance")
        self.saveGraph()

    def addFamily(self, user1, user2):
        """
        Add edge between two users with weight = family
        qual deveria ser a diferenca?
        """
        self.G.addEdge(user1.key, user2.key, weight="family")
        self.G.addEdge(user2.key, user1.key, weight="family")
        self.saveGraph()

    def addClient(self, user1, user2):
        """
        Add edge between two users with weight = client
        """
        self.G.addEdge(user1.key, user2.key, weight="client")
        self.saveGraph()

    def removeClient(self, user1, user2):
        """
        Remove edge between two users
        """
        self.G.removeEdge(user1.key, user2.key)
        self.saveGraph()

    def removeConnection(self, user1, user2):
        """
        Remove edge between two users
        """
        connectionType = self.getConnection(user1, user2)
        self.G.removeEdge(user1.key, user2.key)
        if connectionType in ["friend", "family"]:
            self.G.removeEdge(user2.key, user1.key)
        self.saveGraph()

    def subGraph(self, user, levels):
        """
        Create subgraph centered in user that extends to a certain level of adjacent vertices
        """
        newG = copy.deepcopy(self.G)
        vs = []
        level_vs = [user]
        for i in range(levels):
            next_vs = []
            for vertex in level_vs:
                next_vs += [i[0] for i in vertex.adjacent.values()]
            vs += level_vs
            if not next_vs:
                break
            level_vs = next_vs

        for v in self.G.vertices.values():
            if v not in vs:
                newG.removeVertex(v.key)
        return newG

    def saveGraphImg(self, user, levels=None):
        """
        Create graph in the networkx library
        Save it to image
        """
        if levels:
            subgraph = self.subGraph(user, levels)
        else:
            subgraph = self.G
        DG = nx.DiGraph()
        for node in subgraph.vertices.keys():
            user = self.getUser(node)
            edgeStr = node if 'name' in user.value["private"] else user.value["name"] 
            DG.add_node(edgeStr)
        edges = subgraph.getEdges()

        for v1, v2, w in edges:
            if w == "friend":
                color = "red"
            elif w == "acquaintance":
                color = "blue" 
            elif w == "family":
                color = "green"
            else:
                color = "black"
            user1 = self.getUser(v1)
            user2 = self.getUser(v2)

            edge1Str = v1 if 'name' in user1.value["private"] else user1.value["name"]                
            edge2Str = v2 if 'name' in user2.value["private"] else user2.value["name"]                

            DG.add_edge(edge1Str, edge2Str, color=color)

        pos = nx.circular_layout(DG)
        edges = DG.edges()
        colors = [DG[u][v]['color'] for u, v in edges]
        nx.draw(DG, pos, with_labels=True, edge_color=colors,
                node_color="paleturquoise", arrowsize=20)
        plt.savefig("out/graph.jpg", dpi=1000)
