import numpy as np

class TADGrafo:

    def __init__(self, vertice):
        """ Cria um grafo vazio. """     
        self.vertice = vertice
        self.grafo = np.zeros((vertice,vertice), dtype=int)   

    def InsereAresta(self, V1, V2):
        """ Insere uma aresta no grafo. """
        if(self.grafo[V1, V2] == 1):
            print("Já existe uma aresta entre esses vertices!")
        else:
            self.grafo[V1, V2] = 1

    def ExisteAresta(self, V1, V2):
        """ Verifica se existe uma determinada aresta. """
        if(self.grafo[V1,V2] == 1):
            print("Existe Aresta!")
        else:
            print("Não existe aresta!")
    
    def VerticeAdjacente(self, vertice):
        """ Obtem a lista de vértices adjacentes a um 
        determinado vértice. """
        n = len(self.grafo)
        adj = []
        for i in range(n):
            if self.grafo[vertice][i] == 1:
                adj.append(i)
        return adj

    def RetiraAresta(self, V1, V2):
        """ Retira uma aresta do grafo. """
        if(self.grafo[V1, V2] == 0):
            print("Não existe aresta para remover!")
        else:
            self.grafo[V1, V2] = 0
            print("Aresta removida!")
    
    def LiberaGrafo(self):
        """Liberar o espaço ocupado por um grafo."""
        if(self.grafo is None):
            print("Não está ocupando espaço")
        else:
            self.grafo = None
            print("Grafo liberado")

    def ImprimeGrafo(self):
        """ Imprime um grafo. """
        print(self.grafo)
