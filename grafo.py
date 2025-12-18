from tkinter import messagebox
from collections import deque
import math

def criar_grafo(vertices):
    """Cria uma matriz de adjacência para o grafo"""
    return [[0 for _ in range(vertices)] for _ in range(vertices)]


def adicionar_aresta(grafo, l, c):
    """Adiciona uma aresta não direcionada entre os vértices l e c"""
    if grafo[l - 1][c - 1] == 1 or grafo[c - 1][l - 1] == 1:
        return messagebox.showinfo("Atenção", "Essa aresta já existe")
    else:
        grafo[l - 1][c - 1] = 1
        grafo[c - 1][l - 1] = 1

def remover_aresta(grafo, l, c):
    """Remove uma aresta não direcionada entre os vértices l e c"""
    n = len(grafo)

    if l < 1 or l > n or c < 1 or c > n:
        return messagebox.showinfo("Atenção", "Não existe aresta")
        #return False

    if grafo[l - 1][c - 1] == 0:
        return messagebox.showinfo("Atenção", "Não existe aresta")
        #return False

    grafo[l - 1][c - 1] = 0
    grafo[c - 1][l - 1] = 0
    #return True
    #return messagebox.showinfo("Atenção", "Removido com sucesso")

def existe_aresta(grafo, l, c):
    """Verifica se existe aresta entre l e c"""
    n = len(grafo)

    if l < 1 or l > n or c < 1 or c > n:
        return messagebox.showinfo("Atenção", "Não Existe aresta")
        #return False
    return messagebox.showinfo("Atenção", "Existe aresta")
    #return grafo[l - 1][c - 1] == 1

def vertice_Adjacente(grafo, l):
    return [i + 1 for i in range(len(grafo)) if grafo[l - 1][i] == 1]

# BUSCA EM LARGURA 

def bfs(grafo, inicio, objetivo, debug=False):
    inicio -= 1
    objetivo -= 1

    n = len(grafo)

    fila = deque([inicio])
    cores = ["branco"] * n
    pais = [-1] * n
    distancia = [math.inf] * n

    cores[inicio] = "cinza"
    distancia[inicio] = 0
    pais[inicio] = inicio

    if debug:
        print("=== INÍCIO DA BFS ===")
        print("Fila inicial:", [inicio + 1])

    while fila:
        atual = fila.popleft()

        if debug:
            print(f"\nRetirando {atual + 1} da fila")

        for vizinho in range(n):
            if grafo[atual][vizinho] == 1 and cores[vizinho] == "branco":
                fila.append(vizinho)
                cores[vizinho] = "cinza"
                pais[vizinho] = atual
                distancia[vizinho] = distancia[atual] + 1

                if debug:
                    print(
                        f"Descobriu {vizinho + 1} | "
                        f"Distância: {distancia[vizinho]}"
                    )

        cores[atual] = "preto"

        if debug:
            print(f"Vértice {atual + 1} finalizado (preto)")
            print("Fila:", [v + 1 for v in fila])

        if atual == objetivo:
            break

    # Caminho
    caminho = None
    if pais[objetivo] != -1:
        caminho = []
        v = objetivo
        while v != inicio:
            caminho.append(v + 1)
            v = pais[v]
        caminho.append(inicio + 1)
        caminho.reverse()

    return caminho, cores, pais, distancia

"""g1 = criar_grafo(4)

adicionar_aresta(g1, 1, 2)
adicionar_aresta(g1, 3, 1)
adicionar_aresta(g1, 4, 2)
adicionar_aresta(g1, 3, 2)
print(g1)
print(bfs(g1, 1, 2))"""


