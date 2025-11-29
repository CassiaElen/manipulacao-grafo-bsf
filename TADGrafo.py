class TADGrafo:

    def __init__(self, vertice):
        """ Cria um grafo vazio. """     
        import numpy as np

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
    
    def VerticeAdjacente(self, vertice):
        """ Obtem a lista de vértices adjacentes a um 
        determinado vértice. """

    def RetiraAresta(self, V1, V2):
        """ Retira uma aresta do grafo. """
        if(self.grafo[V1, V2] == 0):
            print("Não existe aresta para remover!")
        else:
            self.grafo[V1, V2] = 0
    
    def LiberaGrafo(self, grafo):
        """Liberar o espaço ocupado por um grafo.
            Apagar o grafo ou os vertices todos os vertices?"""
    
    def ImprimeGrafo(self):
        """ Imprime um grafo. """
        print(self.grafo)

pi = TADGrafo(5)
pi.ImprimeGrafo()
pi.InsereAresta(0,4)
pi.ImprimeGrafo()
pi.ExisteAresta(0,4)
pi.RetiraAresta(2,3)
