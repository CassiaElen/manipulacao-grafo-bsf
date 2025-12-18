import tkinter as tk
import math
from tkinter import messagebox
from random import randint
from TADGrafo import TADGrafo


class Interface:

    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Manipulação de Grafos")
        self.centralizar_janela(800, 600)

        # TAD Grafo
        self.grafo = None
        self.mapa_vertices = {}  # indices
        self.contator_vertices = 0

        # Barra de Menu
        self.create_menu()

        # Canvas para desenhar o grafo
        self.canvas = tk.Canvas(self.janela, bg="#a2cca5")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Dados do grafo para o canvas
        self.vertices = {}  # dicionario
        self.arestas = []  # lista
        self.vertice_selecionado = None

        # Metodos de configuração
        self.vincular_eventos_multiplos()

    def create_graph(self, qtd):
        self.clear_graph()
        self.grafo = TADGrafo(qtd)
        self.create_vertices(qtd)

    def create_vertices(self, qtd):
        """Cria todos os vertices no canvas em posições aleatorias"""

        for name in range(qtd):

            self.mapa_vertices[name] = self.contador_vertices
            self.contador_vertices += 1

            raio = 20  # tamanho fixo do vertice

            largura = self.canvas.winfo_width()
            altura = self.canvas.winfo_height()

            if largura <= 1 or altura <= 1:
                largura, altura = 800, 600

            # Gera posição aleatória garantindo que o vertice não saia da tela
            x = randint(raio, largura - raio)
            y = randint(raio, altura - raio)

            vertice_id = self.canvas.create_oval(
                x - raio,
                y - raio,
                x + raio,
                y + raio,
                fill="lightblue",
                outline="blue",
                width=2,
                tags=("vertice", f"vertice_{name}"),
            )

            text_id = self.canvas.create_text(
                x,
                y,
                text=name,
                font=("Arial", 12, "bold"),
                tags=("vertice_text", f"text_{name}"),
            )

            self.vertices[name] = {
                "id": vertice_id,
                "text": text_id,
                "x": x,
                "y": y,
                "name": name,
                "raio": raio,
            }


    def add_aresta(self, v1, v2):
        """Adiciona uma aresta entre dois vertices"""
        if v1 not in self.mapa_vertices or v2 not in self.mapa_vertices:
            return

        # TAD Grafo
        self.grafo.InsereAresta(self.mapa_vertices[v1], self.mapa_vertices[v2])

        x1 = self.vertices[v1]["x"]
        y1 = self.vertices[v1]["y"]
        x2 = self.vertices[v2]["x"]
        y2 = self.vertices[v2]["y"]

        angulo = math.atan2(y2 - y1, x2 - x1)
        x1 += 20 * math.cos(angulo)
        y1 += 20 * math.sin(angulo)
        x2 -= 20 * math.cos(angulo)
        y2 -= 20 * math.sin(angulo)

        aresta_id = self.canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill="black",
            width=2,
            tags=("aresta", f"aresta_{v1}_{v2}"),
        )

        self.arestas.append({"id": aresta_id, "from": v1, "to": v2})

    # ADICIONAR MAIS UM MEIO DE VERIFICAÇÃO
    def check_aresta(self, v1, v2):
        if v1 not in self.mapa_vertices or v2 not in self.mapa_vertices:
            return

        for aresta in self.arestas:
            if ((aresta["from"] == v1 and aresta["to"] == v2) or
                (aresta["from"] == v2 and aresta["to"] == v1)):
                aresta_id = aresta["id"]

                # muda a cor agora
                self.canvas.itemconfig(aresta_id, fill="red")

                # agenda com o metodo after do tkinter, volta ao normal em 6000 ms (6 s)
                self.janela.after(
                    6000,
                    lambda id=aresta_id: self.canvas.itemconfig(id, fill="black")
                )
                break
        
        self.grafo.ExisteAresta(self.mapa_vertices[v1], self.mapa_vertices[v2])

    def remove_aresta(self, v1, v2):
        if v1 not in self.mapa_vertices or v2 not in self.mapa_vertices:
            return

        self.grafo.RetiraAresta(self.mapa_vertices[v1], self.mapa_vertices[v2])

        for aresta in self.arestas[:]:
            if ((aresta["from"] == v1 and aresta["to"] == v2) or
                (aresta["from"] == v2 and aresta["to"] == v1)):
                self.canvas.delete(aresta["id"])
                self.arestas.remove(aresta)

    def vincular_eventos_multiplos(self):
        """Vincula eventos do mouse ao canvas"""
        self.canvas.bind(
            "<Button-1>", self.encontrar_vertice
        )  # Clique do mouse
        self.canvas.bind(
            "<B1-Motion>", self.arrastar_vertice
        )  # Arrastar com botão pressionado
        self.canvas.bind(
            "<ButtonRelease-1>", self.soltar_vertice
        )  # Soltar botão

    def encontrar_vertice(self, event):
        """Encontra qual vertice foi clicado"""
        # Encontra todos os itens que estão nas coordenadas do clique
        items = self.canvas.find_overlapping(
            event.x - 1, event.y - 1, event.x + 1, event.y + 1
        )

        # Percorre os itens encontrados
        for item in items:
            # Verifica se o item é um dos nossos círculos
            
            for name, vertice in self.vertices.items():
                
                if vertice["id"] == item:
                    # Encontrou uma aresta clicada
                    self.vertice_selecionado = vertice  # Marca como selecionando
                    # Calcula a diferença entre o clique e o centro do círculo
                    self.offset_x = (
                        event.x - self.canvas.coords(item)[0] - vertice["raio"]
                    )
                    self.offset_y = (
                        event.y - self.canvas.coords(item)[1] - vertice["raio"]
                    )
                    return
        # Se não encontrou nenhuma vertice
        self.vertice_selecionado = None

    def arrastar_vertice(self, event):
        """Arrasta o vertice selecionado"""
        if self.vertice_selecionado:  # Se há um vertice sendo arrastado
            # Calcula nova posição baseada no mouse menos o offset
            nova_x = event.x - self.offset_x
            nova_y = event.y - self.offset_y
            raio = self.vertice_selecionado["raio"]

            largura = self.canvas.winfo_width()
            altura = self.canvas.winfo_height()

            # Limita a posição para não sair do canvas
            nova_x = max(raio, min(nova_x, largura - raio))
            nova_y = max(raio, min(nova_y, altura - raio))

            # Move o vertice para a nova posição
            self.canvas.coords(
                self.vertice_selecionado["id"],
                nova_x - raio,
                nova_y - raio,  # Canto superior esquerdo
                nova_x + raio,
                nova_y + raio,  # Canto inferior direito
            )

            self.canvas.coords(
                self.vertice_selecionado["text"],
                nova_x,
                nova_y,
            )
            # Atualiza x e y do vértice armazenado
            self.vertice_selecionado["x"] = nova_x
            self.vertice_selecionado["y"] = nova_y

            self.arrastar_aresta(self.vertice_selecionado["id"])

    def arrastar_aresta(self, vertice_selecionado):
        nome_vertice_selecionado = None
        for name, vertice in self.vertices.items():
            if vertice["id"] == vertice_selecionado:
                nome_vertice_selecionado = name
                break

        if nome_vertice_selecionado is None:
            return

        for aresta in self.arestas:
            if (aresta["from"] == nome_vertice_selecionado or
                aresta["to"] == nome_vertice_selecionado):

                v1 = self.vertices[aresta["from"]]
                v2 = self.vertices[aresta["to"]]

                angulo = math.atan2(v2["y"] - v1["y"], v2["x"] - v1["x"])
                x1 = v1["x"] + 20 * math.cos(angulo)
                y1 = v1["y"] + 20 * math.sin(angulo)
                x2 = v2["x"] - 20 * math.cos(angulo)
                y2 = v2["y"] - 20 * math.sin(angulo)

                self.canvas.coords(aresta["id"], x1, y1, x2, y2)


    def soltar_vertice(self, event):
        """Solta o vertice arrastado"""
        if self.vertice_selecionado:
            # Libera o círculo
            self.vertice_selecionado = None

    def create_menu(self):
        # Barra de menu
        menuBar = tk.Menu(self.janela)
        # Adiciona tudo na barra
        menuBar.add_command(label="Criar Grafo", command=self.create_graph_dialog)
        menuBar.add_command(label="Inserir Aresta", command=self.add_aresta_dialog)
        menuBar.add_command(label="Verificar Aresta", command=self.check_aresta_dialog)
        menuBar.add_command(label="Remover Aresta", command=self.remove_aresta_dialog)
        menuBar.add_command(label="Vertices adjacentes", command=self.vertices_adjacentes_dialog)
        menuBar.add_command(label="Limpar", command=self.clear_graph)
        menuBar.add_command(label="Sair", command=self.janela.quit)

        # Exibir a barra de menus
        self.janela.config(menu=menuBar)

    def create_graph_dialog(self):
        """Diálogo para criar um grafo"""
        dialog = tk.Toplevel(self.janela)
        dialog.title("Criar Grafo")
        dialog.geometry("300x150")

        tk.Label(dialog, text="Quantidade de vertices").pack(pady=5)
        name_entry = tk.Entry(dialog)
        name_entry.pack(pady=5)

        tk.Button(
            dialog,
            text="Criar",
            command=lambda: [
                self.create_graph(int(name_entry.get())),
                dialog.destroy(),
            ],
        ).pack(pady=10)

    def add_aresta_dialog(self):
        """Diálogo para adicionar aresta"""
        if self.grafo is None:
            messagebox.showinfo("Atenção", "Crie um grafo primeiro!")
            return

        dialog = tk.Toplevel(self.janela)
        dialog.title("Adicionar Aresta")
        dialog.geometry("300x190")

        tk.Label(dialog, text="Vertice 1").pack(pady=5)
        entry1 = tk.Entry(dialog)
        entry1.pack(pady=5)
        tk.Label(dialog, text="Vertice 2").pack(pady=5)
        entry2 = tk.Entry(dialog)
        entry2.pack(pady=5)
        tk.Button(
            dialog,
            text="Adicionar",
            command=lambda: [
                self.add_aresta(int(entry1.get()), int(entry2.get())),
                dialog.destroy(),
            ],
        ).pack(pady=10)

    def remove_aresta_dialog(self):
        """Diálogo para adicionar aresta"""
        if self.grafo is None:
            messagebox.showinfo("Atenção", "Crie um grafo primeiro!")
            return
        
        dialog = tk.Toplevel(self.janela)
        dialog.title("Remover Aresta")
        dialog.geometry("300x190")

        tk.Label(dialog, text="Vertice 1").pack(pady=5)
        entry1 = tk.Entry(dialog)
        entry1.pack(pady=5)
        tk.Label(dialog, text="Vertice 2").pack(pady=5)
        entry2 = tk.Entry(dialog)
        entry2.pack(pady=5)
        tk.Button(
            dialog,
            text="Remover",
            command=lambda: [
                self.remove_aresta(int(entry1.get()), int(entry2.get())),
                dialog.destroy(),
            ],
        ).pack(pady=10)

    def check_aresta_dialog(self):
        """Diálogo para adicionar aresta"""
        if self.grafo is None:
            messagebox.showinfo("Atenção", "Crie um grafo primeiro!")
            return
        
        dialog = tk.Toplevel(self.janela)
        dialog.title("Verificar Aresta")
        dialog.geometry("300x190")

        tk.Label(dialog, text="Vertice 1").pack(pady=5)
        entry1 = tk.Entry(dialog)
        entry1.pack(pady=5)
        tk.Label(dialog, text="Vertice 2").pack(pady=5)
        entry2 = tk.Entry(dialog)
        entry2.pack(pady=5)
        tk.Button(
            dialog,
            text="Verificar",
            command=lambda: [
                self.check_aresta(int(entry1.get()), int(entry2.get())),
                dialog.destroy(),
            ],
        ).pack(pady=10)

    def vertices_adjacentes_dialog(self):
        """Diálogo para mostrar os vertices adjacentes"""
        if self.grafo is None:
            messagebox.showinfo("Atenção", "Crie um grafo primeiro!")
            return
        
        dialog = tk.Toplevel(self.janela)
        dialog.title("Verificar adjacentes")
        dialog.geometry("300x190")

        tk.Label(dialog, text="Vertice").pack(pady=5)
        entry1 = tk.Entry(dialog)
        entry1.pack(pady=5)
        tk.Label(dialog, text="Vertices Adjacentes:").pack(pady=5)
        resultado_label = tk.Label(dialog, text="Nenhum vertice")
        resultado_label.pack(pady=5)

        def verificar():
            try:
                v = int(entry1.get())
            except ValueError:
                resultado_label.config(text="Digite um número válido")
                return

            adj = self.grafo.VerticeAdjacente(v)   # retorna lista de vértices
            if adj:
                resultado_label.config(text=", ".join(map(str, adj)))
            else:
                resultado_label.config(text="Nenhum vértice")

        tk.Button(
            dialog,
            text="Verificar",
            command=verificar,
        ).pack(pady=10)

    def clear_graph(self):
        """Limpa tudo, grafo e canvas"""
        self.canvas.delete("all")
        self.vertices.clear()
        self.arestas.clear()
        self.vertice_selecionado = None
        self.mapa_vertices.clear()
        self.contador_vertices = 0
        self.grafo = None

    def centralizar_janela(self, w, h):
        sw = self.janela.winfo_screenwidth()
        sh = self.janela.winfo_screenheight()
        self.janela.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def executar(self):
        self.janela.mainloop()
