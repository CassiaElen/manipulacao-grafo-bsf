from collections import deque

def bfs_menor_caminho_matriz(grafo, inicio, fim):
    n = len(grafo)
    visitado = [False] * n
    anterior = [-1] * n
    fila = deque([inicio])

    visitado[inicio] = True

    while fila:
        atual = fila.popleft()

        if atual == fim:
            break

        # Percorre todos os possíveis vizinhos
        for vizinho in range(n):
            if grafo[atual][vizinho] == 1 and not visitado[vizinho]:
                visitado[vizinho] = True
                anterior[vizinho] = atual
                fila.append(vizinho)

    # Se não visitou o destino, não há caminho
    if not visitado[fim]:
        return None

    # Reconstruir o caminho
    caminho = []
    atual = fim
    while atual != -1:
        caminho.append(atual)
        atual = anterior[atual]

    caminho.reverse()
    return caminho


grafo = [
#    0 1 2 3 4 5
    [0,1,1,0,0,0],  # 0 |  0 -> 1, 2
    [1,0,0,1,0,0],  # 1 |  1 -> 0, 3
    [1,0,0,1,1,0],  # 2 |  2 -> 0, 3, 4
    [0,1,1,0,0,0],  # 3 |  3 -> 1, 2 
    [0,0,1,0,0,1],  # 4 |  4 -> 2, 5
    [0,0,0,0,1,0]   # 5 |  5 -> 4
]


caminho = bfs_menor_caminho_matriz(grafo, 5, 3)
print(caminho)