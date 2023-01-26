import networkx as nx
import matplotlib.pyplot as plt
import pickle

class Vertex:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.adjacent = {}
        self.n_adjacent = 0
        self.n_incident = 0

    def addEdge(self, vertex, weight=0):
        if vertex.key in self.adjacent:
            return 'Vértice já existe'
        else:
            self.adjacent[vertex.key] = (vertex, weight)
            self.n_adjacent += 1
            vertex.n_incident += 1

    def removeEdge(self, vertex):
        if vertex.key in self.adjacent:
            del self.adjacent[vertex.key]
            self.n_adjacent -= 1
            vertex.n_incident -= 1
        else:
            return 'Vértice não existe'

    def redefineEdge(self, vertex, new_w):
        if vertex in self.adjacent:
            self.adjacent[vertex.key] = (vertex, new_w)

    def getConnections(self):
        string = ''
        for adjacentKey in self.adjacent.keys():
            string += f'Relações do nodo {self.key} com o nodo {adjacentKey}: {self.adjacent[adjacentKey]}\n'
        # Retorna o dicionário contendo todas as relações do nodo e uma string interpolada
        return self.adjacent, string

    def formatObj(self):
        keys = self.value.keys()
        copy = {}
        for key in keys:
            copy[key] = self.value[key]
        return copy

    def copyAdj(self):
        keys = self.adjacent().keys()
        copy = {}
        for key in keys:
            copy[key] = self.value[key]
        return copy

    def getRelations(self, weight):
        if (weight in self.adjacent):
            # Retorna as relações com um nodo em específico
            return True, self.adjacent[weight]
        else:
            return False

    def __repr__(self):
        return f"(Key: {self.key}, Value: {self.value}, adjas: {self.adjacent})"

    def __iter__(self):
        for key in self.adjacent.keys():
            yield key, self.adjacent[key]


class Graph:
    def __init__(self):
        self.vertices = {}
        self.n_vertices = 0
        self.n_edges = 0

    def addVertex(self, key, value):
        if key in self.vertices:
            return 'Vértice já existe'
        else:
            vertex = Vertex(key, value)
            self.vertices[key] = vertex
            self.n_vertices += 1

    def removeVertex(self, key):
        if key in self.vertices:
            for vertex in self.vertices.values():
                if key in vertex.adjacent:
                    del vertex.adjacent[key]
            del self.vertices[key]
            self.n_vertices -= 1
        else:
            return 'Vértice não existe no grafo'

    def addEdge(self, start_key, end_key, weight=0, bidirectional=False):
        if start_key in self.vertices and end_key in self.vertices:
            con1 = self.vertices[start_key].addEdge(
                self.vertices[end_key], weight)
            self.n_edges += 1
            if bidirectional:
                con2 = self.vertices[end_key].addEdge(
                    self.vertices[start_key], weight)
                self.n_edges += 1
        else:
            return 'Vértice não existe no grafo'

    def removeEdge(self, start_key, end_key, bidirectional=False):
        if (start_key in self.vertices) and (end_key in self.vertices):
            con1 = self.vertices[start_key].removeEdge(self.vertices[end_key])
            self.n_edges -= 1
            if bidirectional:
                con2 = self.vertices[end_key].removeEdge(
                    self.vertices[start_key])
                self.n_edges -= 1
        else:
            return 'Vértice não existe no grafo'

    def inGraph(self, key):
        return key in self.vertices

    def neighbours(self, start_key, end_key, bidirectional=False):
        return (end_key in self.vertices[start_key].adjacent) or \
               (start_key in self.vertices[end_key].adjacent and bidirectional)

    def getAdjacent(self, key):
        if key in self.vertices:
            return [val[0] for val in self.vertices[key].adjacent.values()]
        else:
            return 'Vértice não existe'

    def getIncident(self, key):
        if key in self.vertices:
            incident = []
            for vertex in self.vertices.values():
                if key in vertex.adjacent:
                    incident.append(vertex)
            return incident
        else:
            return 'Vértice não existe'

    def getEdgeWeight(self, start_key, end_key):
        if (start_key in self.vertices) and (end_key in self.vertices[start_key].adjacent):
            return self.vertices[start_key].adjacent[end_key][1]
        else:
            return None

    def getVertex(self, key):
        if key in self.vertices:
            return self.vertices[key]
        else:
            return None

    def BFS(self, start=None, visible=True, testFunction=None):
        if start:
            if start.key in self.vertices.keys():
                start = self.vertices[start.key]
            else:
                return 'Vértice não existe'
        else:
            start = next(iter(self.vertices.values()))

        queue = [start]
        visited = dict.fromkeys(self.vertices.values(), 0)
        matches = []
        while queue:
            vertex = queue[0]
            del queue[0]
            if not visited[vertex]:
                if testFunction and testFunction(vertex):
                    matches.append(vertex.formatObj())
                visited[vertex] = 1
                queue += [v[0] for v in vertex.adjacent.values()]
        return matches

    def getVertices(self):
        return self.vertices.keys()

    def getEdges(self):
        edges = []
        for key, v in self.vertices.items():
            if v:
                for key2, v2 in v.adjacent.items():
                    edges.append((key, key2, v2[1]))
        return edges

    def dumpToPkl(self, filepath):
        with open(filepath, "wb") as outp:
            pickle.dump(self, outp, pickle.HIGHEST_PROTOCOL)