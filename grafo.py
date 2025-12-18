def criar_grafo(vertices):
    """Cria uma matriz de adjacência para o grafo"""
    grafo = []
    for i in range(vertices):
        linha = []
        for j in range(vertices):
            linha.append(0)
        grafo.append(linha)
    return grafo

def adicionar_aresta(grafo, l, c):
    """Adiciona uma aresta não direcionada entre os vértices u e v"""
    grafo[l-1][c-1] = 1
    grafo[c-1][l-1] = 1

def remover_aresta(grafo, l, c):
    """Remove uma aresta não direcionada entre os vértices l e c"""
    n = len(grafo)
    
    # Verifica se os vértices são válidos
    if l < 1 or l > n or c < 1 or c > n:
        print("Vértice inválido! Não é possível remover aresta.")
        return False
    
    # Verifica se a aresta existe antes de remover
    if grafo[l-1][c-1] == 0:
        print(f"Não existe aresta entre {l} e {c} para remover.")
        return False
    
    # Remove a aresta (ambas direções pois o grafo é não direcionado)
    grafo[l-1][c-1] = 0
    grafo[c-1][l-1] = 0
    
    print(f"Aresta entre {l} e {c} removida com sucesso!")
    return True

def mostrar_matriz(grafo):
    """Exibe a matriz de adjacência do grafo"""
    for linha in grafo:
        print(linha)

    
def existe_aresta(grafo, l, c):
    n = len(grafo)
    if l < 1 or l > n or c < 1 or c > n:
        print("Vértice inválido!")  
        return False
    
    if grafo[l-1][c-1] == 1:
        print("Há aresta!")
        return True
    else:
        print("Não existe aresta")
        return False




#============= BUSCA EM PROFUNDIDADE ======================


from collections import deque

def bfs(grafo, inicio, objetivo):
    
    # Ajusta índices (nossa matriz usa 0, mas os vértices são numerados de 1)
    inicio = inicio - 1
    objetivo = objetivo - 1
    
    # Se for o mesmo vértice
    if inicio == objetivo:
        return [inicio + 1]
    
    # Fila para a busca
    fila = deque([inicio])
    
    # Controle de visitados e pais
    visitados = [False] * len(grafo)
    pais = [-1] * len(grafo)
    
    visitados[inicio] = True
    pais[inicio] = inicio
    
    # Busca principal
    while fila:
        atual = fila.popleft()
        
        # Verifica se encontramos o objetivo
        if atual == objetivo:
            # Reconstrói o caminho
            caminho = []
            v = objetivo
            while v != inicio:
                caminho.append(v + 1)
                v = pais[v]
            caminho.append(inicio + 1)
            caminho.reverse()
            return caminho
        
        # Visita todos os vizinhos
        for vizinho in range(len(grafo)):
            if grafo[atual][vizinho] == 1 and not visitados[vizinho]:
                fila.append(vizinho)
                visitados[vizinho] = True
                pais[vizinho] = atual
    
    # Se chegou aqui, não encontrou caminho
    return None


#mostrar caminho, pais, cores, distancia





g1 = criar_grafo(4)

adicionar_aresta(g1, 1, 2)
adicionar_aresta(g1, 3, 1)
adicionar_aresta(g1, 4, 2)
adicionar_aresta(g1, 3, 2)

mostrar_matriz(g1)

print(bfs(g1, 1, 2))