import numpy as np
from tkinter import messagebox

class TADGrafo:

    def __init__(self, vertice):
        """ Cria um grafo vazio. """     
        self.vertice = vertice
        self.grafo = np.zeros((vertice, vertice), dtype=int)

    def InsereAresta(self, V1, V2):
        """ Insere uma aresta no grafo. """
        if self.grafo[V1][V2] == 1 or self.grafo[V2][V1] == 1:
            return messagebox.showinfo("Atenção", "Essa aresta já existe")
        else:
            self.grafo[V1][V2] = 1
            self.grafo[V2][V1] = 1

    def ExisteAresta(self, V1, V2):
        """ Verifica se existe uma determinada aresta. """
        if self.grafo[V1][V2] == 1 or self.grafo[V2][V1] == 1:
            return messagebox.showinfo("Atenção", "Existe aresta")
        else:
            return messagebox.showinfo("Atenção", "Não existe aresta")

    def VerticeAdjacente(self, V):
        """ Obtem a lista de vértices adjacentes a um 
        determinado vértice. """
        verticesAdjacentes = [i for i in range(self.vertice) if self.grafo[V][i] == 1]
        return verticesAdjacentes #messagebox.showinfo("Vertices Adjacentes", verticesAdjacentes)
    
    def RetiraAresta(self, V1, V2):
        """ Retira uma aresta do grafo. """
        if self.grafo[V1][V2] == 0 or self.grafo[V2][V1] == 0:
            return messagebox.showinfo("Atenção", "Não existe aresta")
        else:
            self.grafo[V1][V2] = 0
            self.grafo[V2][V1] = 0

    def LiberaGrafo(self):
        """Liberar o espaço ocupado por um grafo."""
        self.grafo = None

    def ImprimeGrafo(self):
        """ Imprime um grafo. """
        print(self.grafo)
"""
pi = TADGrafo(6)
pi.ImprimeGrafo()
print("---------------------------------------")
pi.InsereAresta(0,1)
pi.InsereAresta(0,2)
pi.InsereAresta(1,3)
pi.InsereAresta(2,3)
pi.InsereAresta(2,4)
pi.InsereAresta(5,4)
pi.ImprimeGrafo()
print("---------------------------------------")
print(pi.VerticeAdjacente(2))



grafo = [
#    0 1 2 3 4 5
    [0,1,1,0,0,0],  # 0 |  0 -> 1, 2
    [1,0,0,1,0,0],  # 1 |  1 -> 0, 3
    [1,0,0,1,1,0],  # 2 |  2 -> 0, 3, 4
    [0,1,1,0,0,0],  # 3 |  3 -> 1, 2 
    [0,0,1,0,0,1],  # 4 |  4 -> 2, 5
    [0,0,0,0,1,0]   # 5 |  5 -> 4
]"""