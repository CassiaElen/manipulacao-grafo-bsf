import tkinter as tk

class interface:

    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Manipulação de Grafos")
        self.centralizar_janela(800,600)
        
        #menu
        self.create_menu()

        # Canvas para desenhar o grafo
        self.canvas = tk.Canvas(self.janela, bg='#a2cca5')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Dados do grafo
        self.nodes = {} # dicionario
        self.edges = [] # lista
        self.selected_node = None

        # Eventos do mouse
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_node_drag)

    def add_node(self, name):
        """ Adiciona um nó ao grafo em posição aleatória"""
        from random import randint

        raio = 20# Tamanho fixo do círculo

        # Gera posição aleatória garantindo que o círculo não saia da tela
        x = randint(raio, 700 - raio)
        y = randint(raio, 500 - raio)

        node_id = self.canvas.create_oval(
            x - raio, y - raio,
            x + raio, y + raio,             
            fill="lightblue",
            outline="blue",
            width=2,
            tags=("node", f"node_{name}"),
        )

        text_id = self.canvas.create_text(
            x,
            y,
            text=name,
            fill="black",
            font=("Arial", 12, "bold"),
            tags=("node_text", f"text_{name}"),
        )

        self.nodes[name] = {
            "id" : node_id,
            "text_id": text_id,
            "x" : x,
            "y" : y,
            "name":name,
        }

    def add_edge(self, node1, node2):
        """Adiciona uma aresta entre dois nós"""
        import math

        if node1 not in self.nodes or node2 not in self.nodes:
            return
        
        x1, y1 = self.nodes[node1]["x"], self.nodes[node1]["y"] 
        x2, y2 = self.nodes[node2]["x"], self.nodes[node2]["y"]

        angle = math.atan2(y2 - y1, x2 - x1)
        x1_adj = x1 + 20 * math.cos(angle)     
        y1_adj = y1 + 20 * math.sin(angle) 
        x2_adj = x2 + 20 * math.cos(angle) 
        y2_adj = y2 + 20 * math.sin(angle)

        edge_id = self.canvas.create_line(
            x1_adj,
            y1_adj,
            x2_adj,
            y2_adj,
            fill="black",
            width=2,
            tags=("edge", f"edge_{node1}_{node2}"),
        )                

        self.edges.append(
            {
                "id": edge_id,
                "from": node1,
                "to": node2,
            }
        )
    def remove_edge():
        return
    def on_canvas_click(self, event):
        """Lida com cliques no canvas"""
        # Verifica se clicou em um nó
        clicked_items = self.canvas.find_overlapping(
            event.x-5, event.y-5, event.x+5, event.y+5
        )
        
        for item in clicked_items:
            tags = self.canvas.gettags(item)
            if "node" in tags and "node_text" not in tags:
                for tag in tags:
                    if tag.startswith("node_"):
                        node_name = tag[5:]
                        self.selected_node = node_name
                        self.highlight_node(node_name)
                        return
        
        self.selected_node = None
    
    def on_node_drag(self, event):
        """Arrasta um nó"""
        if self.selected_node and self.selected_node in self.nodes:
            node = self.nodes[self.selected_node]

            # Atualiza posição do nó
            self.canvas.coords(
                node["id"], event.x - 20, event.y - 20, event.x + 20, event.y + 20
            )
            self.canvas.coords(node["text_id"], event.x, event.y)

            node["x"] = event.x
            node["y"] = event.y

            # Atualiza todas as arestas conectadas
            self.update_edges(self.selected_node)

    def update_edges(self, node_name):
        """Atualiza as arestas conectadas a um nó"""
        import math

        for edge in self.edges:
            if edge["from"] == node_name or edge["to"] == node_name:
                node1 = self.nodes[edge["from"]]
                node2 = self.nodes[edge["to"]]

                x1, y1 = node1["x"], node1["y"]
                x2, y2 = node2["x"], node2["y"]

                # Recalcula posições ajustadas
                angle = math.atan2(y2 - y1, x2 - x1)
                x1_adj = x1 + 20 * math.cos(angle)
                y1_adj = y1 + 20 * math.sin(angle)
                x2_adj = x2 - 20 * math.cos(angle)
                y2_adj = y2 - 20 * math.sin(angle)

                # Atualiza a linha
                self.canvas.coords(edge["id"], x1_adj, y1_adj, x2_adj, y2_adj)

    def highlight_node(self, node_name):
        """Destaca um nó"""

        for name, node in self.nodes.items():
            self.canvas.itemconfig(node["id"], fill="lightblue")
        if node_name in self.nodes:
            self.canvas.itemconfig(self.nodes[node_name]["id"], fill="yellow")

    def add_node_dialog(self):
        """Diálogo para adicionar nó"""
        dialog = tk.Toplevel(self.janela)
        dialog.title("Adicionar Nó")
        dialog.geometry("300x150")

        tk.Label(dialog, text="Nome do nó:").pack(pady=5)
        name_entry = tk.Entry(dialog)
        name_entry.pack(pady=5)

        def submit():
            name = name_entry.get()
            if name:
                self.add_node(name)
                dialog.destroy()
        
        tk.Button(dialog, text="Adicionar", command=submit).pack(pady=10)

    def add_edge_dialog(self):
        """Diálogo para adicionar aresta"""
        dialog = tk.Toplevel(self.janela)
        dialog.title("Adicionar Aresta")
        dialog.geometry("300x200")
        
        tk.Label(dialog, text="Primeiro Nó:").pack(pady=5)
        from_entry = tk.Entry(dialog)
        from_entry.pack(pady=5)
        
        tk.Label(dialog, text="Segundo Nó:").pack(pady=5)
        to_entry = tk.Entry(dialog)
        to_entry.pack(pady=5)
        
        def submit():
            from_node = from_entry.get()
            to_node = to_entry.get()
            
            if from_node and to_node:
                self.add_edge(from_node, to_node)
                dialog.destroy()
        
        tk.Button(dialog, text="Adicionar", command=submit).pack(pady=10)

    def remove_edge_dialog(self):
        return
    
    def check_edge_dialog(self):
        return
    
    def clear_canvas(self):
        """Limpa todo o canvas"""
        self.canvas.delete("all")
        self.nodes.clear()
        self.edges.clear()
        self.selected_node = None  

    def create_menu(self):
        # Barra de menu
        menuBar =  tk.Menu(self.janela)

        # ----- MENU AJUDA -----
        menu_ajuda = tk.Menu(menuBar, tearoff=0)
        menu_ajuda.add_command(label="Sobre", )

        # Adiciona tudo na barra
        menuBar.add_command(label="Criar Grafo")
        menuBar.add_command(label="Adicionar Nó", command=self.add_node_dialog)

        menuBar.add_command(label="Inserir Aresta", command=self.add_edge_dialog)
        menuBar.add_command(label="Verificar Aresta", command=self.check_edge_dialog)
        menuBar.add_command(label="Remover Aresta", command=self.remove_edge_dialog)
        # fazer junção com o metodo LiberaGrafo
        menuBar.add_command(label="Limpar", command=self.clear_canvas)
        menuBar.add_cascade(label="Ajuda", menu=menu_ajuda)
        menuBar.add_command(label="Sair", command=self.janela.quit)

        # Exibir a barra de menus
        self.janela.config(menu=menuBar)

    def centralizar_janela(self, largura, altura):
        largura_tela = self.janela.winfo_screenwidth()
        altura_tela = self.janela.winfo_screenheight()

        x = (largura_tela - largura) // 2
        y = (altura_tela - altura) // 2

        self.janela.geometry(f"{largura}x{altura}+{x}+{y}")

    def executar(self):
        self.janela.mainloop()
