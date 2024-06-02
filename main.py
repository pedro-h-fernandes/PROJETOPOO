import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime


class Tarefa:  # Criar tarefas
    def __init__(self):
        self.conn = sqlite3.connect('data.db')

    def abrir_tela(self):
        janela = tk.Toplevel()
        janela.title("Criação de Tarefa")
        Sistema.centralizar_janela(janela, 400, 300)
        tk.Label(janela, text="Bem-vindo, Gestor!",
                 font=("Helvetica", 16)).pack(pady=20)

    def ver_tarefas(self, coletor_id):
        janela = tk.Toplevel()
        janela.title("Tarefas")
        Sistema.centralizar_janela(janela, 400, 300)
        tk.Label(janela, text="Bem-vindo, Coletor!",
                 font=("Helvetica", 16)).pack(pady=20)

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT descricao, data, hora, local FROM tarefa WHERE coletor_id=?", (coletor_id,))
        tarefas = cursor.fetchall()

        if tarefas:
            for tarefa in tarefas:
                descricao, data, hora, local = tarefa
                tk.Label(janela, text=f"{data} - {descricao}\nHora: {hora}\nLocal: {local}",
                         bg="#f0f0f0", fg="#333333", font=("Helvetica", 12)).pack(pady=20)
        else:
            tk.Label(janela, text="Nenhuma tarefa encontrada.",
                     bg="#f0f0f0", fg="#333333", font=("Helvetica", 12)).pack(pady=20)


class Relatorio:  # Criar relatorio para o gestor
    def __init__(self):
        self.conn = sqlite3.connect('data.db')

    def abrir_tela(self):
        janela = tk.Toplevel()
        janela.title("Estoque")
        Sistema.centralizar_janela(janela, 500, 400)
        janela.configure(bg="#f0f0f0")

        tk.Label(janela, text="Relatório", bg="#f0f0f0",
                 fg="#333333", font=("Helvetica", 16)).pack(pady=20)

        entries = {}
        campos = ["titulo", "descricao", "data do relatorio",
                  "Quantidade de coletas", "quantidade coletada"]
        y_positions = [60, 90, 120, 150, 180]

        for campo, y in zip(campos, y_positions):
            tk.Label(janela, text=f"{campo.capitalize()}:", bg="#f0f0f0", fg="#333333", font=(
                "Helvetica", 12)).place(x=30, y=y)
            entry = tk.Entry(janela, font=("Helvetica", 12),
                             show="*" if campo == "password" else None)
            entry.place(x=250, y=y)
            entries[campo] = entry

        # Adicionando Radiobuttons para os tipos de materiais
        tipos_material = ["Plastico", "Vidro", "Metal", "Papel"]
        self.tipo_material_var = tk.StringVar()
        for i, tipo_material in enumerate(tipos_material):
            tk.Radiobutton(janela, text=tipo_material, variable=self.tipo_material_var, value=tipo_material,
                           bg="#f0f0f0", fg="#333333", font=("Helvetica", 12)).place(x=30, y=230 + i*30)

        tk.Button(janela, text="Gerar Relatório", bg="#4CAF50", fg="#ffffff", font=("Helvetica", 12),
                  command=lambda: self.gerar_relatorio(janela, entries)).place(x=250, y=200 + len(tipos_material)*30)

    def gerar_relatorio(self, nova_janela, entries):
        titulo = entries['titulo'].get()
        descricao = entries['descricao'].get()
        data = entries['data do relatorio'].get()
        qtd_coletas = entries['Quantidade de coletas'].get()
        qtd_coletada = entries['quantidade coletada'].get()
        tipo_material = self.tipo_material_var.get()
        tipo_material = tipo_material.lower()

        if all([titulo, descricao, data, qtd_coletas, qtd_coletada, tipo_material]):
            self.conn.execute("INSERT INTO relatorio_mensal (titulo, descricao, data_relatorio, qtd_coletas, qtd_coletada, tipo_material) VALUES (?, ?, ?, ?, ?, ?)",
                              (titulo, descricao, data, qtd_coletas, qtd_coletada, tipo_material))
            self.conn.commit()
            messagebox.showinfo(
                "Cadastro", "Relatório cadastrado com sucesso!")
            nova_janela.destroy()
        else:
            messagebox.showerror(
                "Cadastro", "Por favor, preencha todos os campos.")

    def tela_relatorio_por_tipo(self, tipo_material):
        nova_janela = tk.Toplevel()
        nova_janela.title(f"Relatório de {tipo_material}")
        Sistema.centralizar_janela(nova_janela, 400, 400)
        nova_janela.configure(bg="#f0f0f0")

        tk.Label(nova_janela, text=f"Relatório de {tipo_material}", bg="#f0f0f0", fg="#333333",
                 font=("Helvetica", 16)).pack(pady=20)

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT titulo, descricao, data, qtd_coletas, qtd_coletada, tipo_material FROM relatorio_mensal WHERE tipo_material=?", (tipo_material,))
        relatorios = cursor.fetchall()
        for relatorio in relatorios:
            titulo, descricao, data, qtd_coletas, qtd_coletada, tipo_material = relatorio
            tk.Label(nova_janela, text=f"{data} - {titulo}\nDescrição: {descricao}\nQuantidade de coletas: {qtd_coletas}\nQuantidade coletada: {qtd_coletada}\nTipo de material: {tipo_material}",
                     bg="#f0f0f0", fg="#333333", font=("Helvetica", 12)).pack(pady=20)


class Estoque:  # Criar e gerenciar o estoque
    def __init__(self):
        self.conn = sqlite3.connect('data.db')

    def abrir_tela(self):
        janela = tk.Toplevel()
        janela.title("Estoque")
        Sistema.centralizar_janela(janela, 400, 500)
        janela.configure(bg="#f0f0f0")

        tk.Label(janela, text="Estoque", bg="#f0f0f0", fg="#333333",
                 font=("Helvetica", 16)).pack(pady=20)

        tk.Button(janela, text="Plástico", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12), command=self.monitorar_plastico).pack(pady=30)
        tk.Button(janela, text="Vidro", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12), command=self.monitorar_vidro).pack(pady=32)
        tk.Button(janela, text="Metal", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12), command=self.monitorar_metal).pack(pady=34)
        tk.Button(janela, text="Papel", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12), command=self.monitorar_papel).pack(pady=36)

    def buscar_dados_estoque(self, tipo_material):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT quantidade_atual, capacidade_max, local FROM estoque WHERE tipo_material=?", (tipo_material,))
        resultado = cursor.fetchone()

        if resultado is None:
            messagebox.showerror(
                "Erro", f"Não há dados de estoque para {tipo_material}")
        else:
            quantidade_atual, capacidade_max, local = resultado
        messagebox.showinfo(
            "Estoque", f"Quantidade atual de {tipo_material}: {quantidade_atual}\nCapacidade máxima: {capacidade_max}\n Local: {local}")

    def monitorar_plastico(self):
        self.buscar_dados_estoque("plastico")

    def monitorar_vidro(self):
        self.buscar_dados_estoque("vidro")

    def monitorar_metal(self):
        self.buscar_dados_estoque("metal")

    def monitorar_papel(self):
        self.buscar_dados_estoque("papel")


class Usuario:  # Configuração inicial Usuario generico
    def __init__(self, id, username, password, cpf, email, nome, telefone, tipo):
        self.id = id
        self.username = username
        self.password = password
        self.cpf = cpf
        self.email = email
        self.nome = nome
        self.telefone = telefone
        self.tipo = tipo
        self.conn = sqlite3.connect('data.db')


class Gestor(Usuario):  # Criar e gerir a aba e função do gestor
    def __init__(self, id, username, password, cpf, email, nome, telefone):
        super().__init__(id, username, password, cpf, email, nome, telefone, "Gestor")

    def abrir_tela(self):
        janela = tk.Toplevel()
        janela.title("Tela do Gestor")
        Sistema.centralizar_janela(janela, 400, 500)
        tk.Label(janela, text="Bem-vindo, Gestor!",
                 font=("Helvetica", 16)).pack(pady=20)

        tk.Button(janela, text="Cadastrar Coletor", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12), command=self.cadastrar_coletor).pack(pady=20)

        tk.Button(janela, text="Criar Tarefa", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12), command=self.criar_tarefa).pack(pady=30)

        tk.Button(janela, text="Gerar Relatório", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12), command=self.gerar_relatorio).pack(pady=35)

        tk.Button(janela, text="Monitorar Estoque", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12), command=self.monitorarEstoque).pack(pady=40)

    def cadastrar_coletor(self):
        Sistema.abrir_janela_cadastro_gestor(self)

    def criar_tarefa(self):
        Sistema.abrir_janela_criar_tarefa(self)

    def gerar_relatorio(self):
        relatorio = Relatorio()
        relatorio.abrir_tela()

    def monitorarEstoque(self):
        estoque = Estoque()
        estoque.abrir_tela()


class Coordenador(Usuario):  # Criar e gerir a aba e função do gestor

    def __init__(self, id, username, password, cpf, email, nome, telefone):
        super().__init__(id, username, password, cpf, email, nome, telefone, "Coordenador")

    def abrir_tela(self):
        janela = tk.Toplevel()
        janela.title("Tela do Coordenador")
        Sistema.centralizar_janela(janela, 400, 300)
        tk.Label(janela, text="Bem-vindo, Coordenador!",
                 font=("Helvetica", 16)).pack(pady=20)

        tk.Button(janela, text="Ver Relatorio", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12), command=self.ver_relatorio).pack(pady=20)
        tk.Button(janela, text="Cadastrar Coletor", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12), command=self.cadastrar_gestor).pack(pady=20)
        tk.Button(janela, text="Cadastrar Empresa", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12), command=self.cadastrar_empresa).pack(pady=20)
        tk.Button(janela, text="Gerar relatorio", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12), command=self.gerar_relatorio_mensal).pack(pady=20)

    def cadastrar_gestor(self):
        Sistema.abrir_janela_cadastro_coordenador(self)

    def cadastrar_empresa(self):
        Sistema.abrir_janela_cadastro_empresa(self)

    def ver_relatorio(self):
        relatorio = Relatorio()

        janela = tk.Toplevel()
        janela.title("Relatório")
        Sistema.centralizar_janela(janela, 400, 500)
        janela.configure(bg="#f0f0f0")

        tk.Label(janela, text="Relatorio", bg="#f0f0f0", fg="#333333",
                 font=("Helvetica", 16)).pack(pady=20)

        tk.Button(janela, text="Plástico", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12)).pack(pady=30)

        tk.Button(janela, text="metal", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12)).pack(pady=30)

        tk.Button(janela, text="vidro", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12)).pack(pady=30)

        tk.Button(janela, text="papel", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12)).pack(pady=30)


class Coletor(Usuario):  # Criar e gerir a aba e função do gestor
    def __init__(self, id, username, password, cpf, email, nome, telefone, ):
        super().__init__(id, username, password, cpf, email, nome, telefone, "Coletor")

    def cadastrar_coleta(self):
        Sistema.abrir_janela_coleta(self)

    def abrir_tela(self):
        janela = tk.Toplevel()
        janela.title("Tela do Coletor")
        Sistema.centralizar_janela(janela, 400, 500)

        tk.Label(janela, text="Bem-vindo, Coletor!",
                 font=("Helvetica", 16)).pack(pady=20)
        tk.Button(janela, text="Cadastrar Coleta", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12), command=self.cadastrar_coleta).pack(pady=40)

        tk.Button(janela, text="Ver tarefas", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12), command=self.tarefas_view).pack(pady=43)

        tk.Button(janela, text="Alerta de estoque", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12), command=self.alertar_gestor).pack(pady=43)

    def tarefas_view(self):
        tarefa = Tarefa()
        tarefa.ver_tarefas(self.id)

    def alertar_gestor(self):
        messagebox.showinfo(
            "Enviado", "Alerta de estoque foi enviado com sucesso!")

    # def tarefas_view(self):


class Sistema:  # Funcoes de funcionamento da aplicação e gerir banco de dados
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.centralizar_janela(self.root, 500, 250)
        self.root.configure(bg="#f0f0f0")

        self.conn = sqlite3.connect('data.db')
        self.criar_tabelas()
        self.inserir_users_padrao()

        self.username_entry = self.criar_campo(
            self.root, "Nome de usuário:", 30, 30)
        self.password_entry = self.criar_campo(
            self.root, "Senha:", 70, 30, show="*")

        self.tipo_usuario = tk.StringVar(value="")

        tipos = ["Gestor", "Coordenador", "Coletor"]
        y_tipo_positions = [120, 150, 180]

        for tipo, y in zip(tipos, y_tipo_positions):
            tk.Radiobutton(self.root, text=tipo, bg="#f0f0f0", fg="#333333",
                           variable=self.tipo_usuario, value=tipo, font=("Helvetica", 12)).place(x=300, y=y)

        tk.Button(self.root, text="Login", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12), command=self.login).place(x=80, y=120)
        tk.Button(self.root, text="Cadastrar", bg="#4CAF50", fg="#ffffff", font=(
            "Helvetica", 12), command=self.abrir_janela_cadastro).place(x=150, y=120)

    def criar_tabelas(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS gestor
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              username TEXT NOT NULL,
                              password TEXT NOT NULL,
                              cpf TEXT NOT NULL UNIQUE,
                              email TEXT NOT NULL,
                              nome TEXT NOT NULL,
                              telefone TEXT NOT NULL)''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS coordenador
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              username TEXT NOT NULL,
                              password TEXT NOT NULL,
                              cpf TEXT NOT NULL UNIQUE,
                              email TEXT NOT NULL,
                              nome TEXT NOT NULL,
                              telefone TEXT NOT NULL)''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS coletor
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              username TEXT NOT NULL,
                              password TEXT NOT NULL,
                              cpf TEXT NOT NULL UNIQUE,
                              email TEXT NOT NULL,
                              nome TEXT NOT NULL,
                              telefone TEXT NOT NULL)''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS coletas
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          coletor_id INTEGER NOT NULL,
                          data TEXT NOT NULL,
                          tipo_material TEXT NOT NULL UNIQUE,
                          quantidade REAL NOT NULL,
                          local TEXT NOT NULL,
                          destino_final TEXT NOT NULL,
                          FOREIGN KEY (coletor_id) REFERENCES usuarios(id))''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS tarefa
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            descricao TEXT NOT NULL,
                            data DATE NOT NULL,
                            hora TIME NOT NULL,
                            local TEXT NOT NULL,
                            Coletor_id INTEGER NOT NULL,
                            FOREIGN KEY (Coletor_id) REFERENCES usuarios(id))
                          ''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS estoque (
                            cod_armazen INTEGER PRIMARY KEY AUTOINCREMENT,
                            tipo_material TEXT NOT NULL UNIQUE,
                            quantidade_atual REAL NOT NULL,
                            capacidade_max REAL NOT NULL,
                            local TEXT NOT NULL)
                        ''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS empresa
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              nome TEXT NOT NULL,
                              email TEXT NOT NULL,
                              cnpj TEXT NOT NULL UNIQUE,
                              cidade TEXT NOT NULL,
                              estado TEXT NOT NULL,
                              telefone TEXT NOT NULL)''')

        # Relatorio {data} - {titulo}\n descricao: {desricao}\n qtd_coletas: {qtd_coletas}\n qtd_coletada: {qtd_coletada}\n tipo_material: {tipo_material}

        self.conn.execute(''' CREATE TABLE IF NOT EXISTS relatorio_mensal (
                            cod_relatorio INTEGER PRIMARY KEY AUTOINCREMENT,
                            titulo TEXT NOT NULL,
                            descricao TEXT NOT NULL,
                            data_relatorio DATE NOT NULL,
                            qtd_coletas REAL NOT NULL,
                            qtd_coletada REAL NOT NULL,
                            tipo_material TEXT NOT NULL

        )''')

    # faz o controle dos users padrao
        self.conn.execute('''CREATE TABLE IF NOT EXISTS controle_inserts
                         (tabela TEXT PRIMARY KEY,
                          inserido INTEGER NOT NULL)''')

        self.conn.commit()

    def inserir_users_padrao(self):
        res = self.conn.execute(
            '''SELECT inserido FROM controle_inserts WHERE tabela = 'gestor' ''').fetchone()
        if res is None:
            self.conn.execute('''INSERT INTO gestor (username, password, cpf, email, nome, telefone)
                                VALUES (?, ?, ?, ?, ?, ?)''',
                              ('adminG', 'adminG', '123342456789', 'gestor@email.com', 'Dolenc', '19999999999'))
            self.conn.execute(
                '''INSERT INTO controle_inserts (tabela, inserido) VALUES (?, ?)''', ('gestor', 1))

        res = self.conn.execute(
            '''SELECT inserido FROM controle_inserts WHERE tabela = 'coordenador' ''').fetchone()
        if res is None:
            self.conn.execute('''INSERT INTO coordenador (username, password, cpf, email, nome, telefone)
                                VALUES (?, ?, ?, ?, ?, ?)''',
                              ('admin', 'admin', '12345678901', 'coordenador@email.com', 'Pedro', '12 212121212'))
            self.conn.execute(
                '''INSERT INTO controle_inserts (tabela, inserido) VALUES (?, ?)''', ('coordenador', 1))

        res = self.conn.execute(
            '''SELECT inserido FROM controle_inserts WHERE tabela = 'estoque' ''').fetchone()
        if res is None:
            self.conn.execute('''INSERT INTO estoque (tipo_material, quantidade_atual, capacidade_max, local)
                                VALUES (?, ?, ?, ?)''',
                              ('plastico', '0', '2000', 'Ecopoint plastico'))

            self.conn.execute('''INSERT INTO estoque (tipo_material, quantidade_atual, capacidade_max, local)
                                VALUES (?, ?, ?, ?)''',
                              ('vidro', '0', '2000', 'Ecopoint vidro'))

            self.conn.execute('''INSERT INTO estoque (tipo_material, quantidade_atual, capacidade_max, local)
                                VALUES (?, ?, ?, ?)''',
                              ('papel', '0', '2000', 'Ecopoint papel'))

            self.conn.execute('''INSERT INTO estoque (tipo_material, quantidade_atual, capacidade_max, local)
                                VALUES (?, ?, ?, ?)''',
                              ('metal', '0', '2000', 'Ecopoint metal'))
            self.conn.execute(
                '''INSERT INTO controle_inserts (tabela, inserido) VALUES (?, ?)''', ('estoque', 1))

        self.conn.commit()

    @staticmethod
    def centralizar_janela(janela, width, height):
        screen_width = janela.winfo_screenwidth()
        screen_height = janela.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        janela.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def criar_campo(self, janela, texto, y, x, show=None):
        tk.Label(janela, text=texto, bg="#f0f0f0", fg="#333333",
                 font=("Helvetica", 12)).place(x=30, y=y)
        entry = tk.Entry(janela, show=show, font=("Helvetica", 12))
        entry.place(x=250, y=y)
        return entry

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        tipo_usuario = self.tipo_usuario.get()
        tipo_usuario = tipo_usuario.lower()

        cursor = self.conn.cursor()
        cursor.execute(
            f"SELECT * FROM {tipo_usuario} WHERE username=? AND password=?", (username, password, ))

        usuario_data = cursor.fetchone()

        if usuario_data:
            self.abrir_tela_usuario(usuario_data)
        else:
            messagebox.showerror(
                "Login", "Nome de usuário ou senha incorretos.")

    def abrir_tela_usuario(self, usuario_data):
        self.root.withdraw()
        id, username, password, cpf, email, nome, telefone = usuario_data
        # Add this line to declare the missing variable
        tipo_usuario = self.tipo_usuario.get()

        if tipo_usuario == "Gestor":
            Gestor(id, username, password, cpf,
                   email, nome, telefone).abrir_tela()
        elif tipo_usuario == "Coordenador":
            Coordenador(id, username, password, cpf,
                        email, nome, telefone).abrir_tela()
        elif tipo_usuario == "Coletor":
            Coletor(id, username, password, cpf,
                    email, nome, telefone).abrir_tela()

    def abrir_janela_cadastro(self):
        nova_janela = tk.Toplevel()
        nova_janela.title("Cadastro de Usuário")
        self.centralizar_janela(nova_janela, 400, 400)
        nova_janela.configure(bg="#f0f0f0")

        entries = {}
        campos = ["username", "password", "cpf", "email", "nome", "telefone"]
        y_positions = [30, 60, 90, 120, 150, 180]

        for campo, y in zip(campos, y_positions):
            tk.Label(nova_janela, text=f"{campo.capitalize()}:", bg="#f0f0f0", fg="#333333", font=(
                "Helvetica", 12)).place(x=30, y=y)
            entry = tk.Entry(nova_janela, font=("Helvetica", 12),
                             show="*" if campo == "password" else None)
            entry.place(x=150, y=y)
            entries[campo] = entry

        tk.Label(nova_janela, text="Tipo de Usuário:", bg="#f0f0f0",
                 fg="#333333", font=("Helvetica", 12)).place(x=30, y=210)
        tipo_var = tk.StringVar(value="")

        tipos = ["Gestor", "Coordenador"]
        y_tipo_positions = [210, 240, 270]

        for tipo, y in zip(tipos, y_tipo_positions):
            tk.Radiobutton(nova_janela, text=tipo, bg="#f0f0f0", fg="#333333",
                           variable=tipo_var, value=tipo, font=("Helvetica", 12)).place(x=180, y=y)

        tk.Button(nova_janela, text="Cadastrar", bg="#4CAF50", fg="#ffffff", font=("Helvetica", 12),
                  command=lambda: self.cadastrar_usuario(nova_janela, entries, tipo_var)).place(x=150, y=320)

    @staticmethod
    def abrir_janela_coleta(self):
        nova_janela = tk.Toplevel()
        nova_janela.title("Cadastro de Coleta")
        Sistema.centralizar_janela(nova_janela, 400, 400)
        nova_janela.configure(bg="#f0f0f0")

        entries = {}
        campos = ["coletor_id", "data", "tipo_material",
                  "quantidade", "local", "destino_final"]
        y_positions = [30, 60, 90, 120, 150, 180]

        for campo, y in zip(campos, y_positions):
            tk.Label(nova_janela, text=f"{campo.capitalize()}:", bg="#f0f0f0", fg="#333333", font=(
                "Helvetica", 12)).place(x=30, y=y)
            entry = tk.Entry(nova_janela, font=("Helvetica", 12),
                             show="*" if campo == "password" else None)
            entry.place(x=150, y=y)
            entries[campo] = entry

        tk.Button(nova_janela, text="Cadastrar", bg="#4CAF50", fg="#ffffff", font=("Helvetica", 12),
                  command=lambda: Sistema.cadastrar_coleta(self, nova_janela, entries)).place(x=150, y=220)

    @staticmethod
    def cadastrar_coleta(self, nova_janela, entries):
        coletor_id = entries['coletor_id'].get()
        data = entries['data'].get()
        tipo_material = entries['tipo_material'].get()
        quantidade = entries['quantidade'].get()
        local = entries['local'].get()
        destino_final = entries['destino_final'].get()

        if all([coletor_id, data, tipo_material, quantidade, local]):
            self.conn.execute("INSERT INTO coletas  (coletor_id, data, tipo_material, quantidade, local, destino_final) VALUES (?, ?, ?, ?, ?, ?)",
                              (coletor_id, data, tipo_material, quantidade, local, destino_final))
            self.conn.commit()
# Atualiza a quantidade de material no estoque
            self.conn.execute(
                "UPDATE estoque SET quantidade_atual = quantidade_atual + ? WHERE tipo_material = ?", (quantidade, tipo_material))
            self.conn.commit()
            messagebox.showinfo("Cadastro", "Coleta cadastrada com sucesso!")
            nova_janela.destroy()
        else:
            messagebox.showerror(
                "Cadastro", "Por favor, preencha todos os campos.")

    @staticmethod
    def abrir_janela_cadastro_gestor(self):
        nova_janela = tk.Toplevel()
        nova_janela.title("Cadastro de Coletor")
        Sistema.centralizar_janela(nova_janela, 400, 400)
        nova_janela.configure(bg="#f0f0f0")

        entries = {}
        campos = ["username", "password", "cpf", "email", "nome", "telefone"]
        y_positions = [30, 60, 90, 120, 150, 180]

        for campo, y in zip(campos, y_positions):
            tk.Label(nova_janela, text=f"{campo.capitalize()}:", bg="#f0f0f0", fg="#333333", font=(
                "Helvetica", 12)).place(x=30, y=y)
            entry = tk.Entry(nova_janela, font=("Helvetica", 12),
                             show="*" if campo == "password" else None)
            entry.place(x=150, y=y)
            entries[campo] = entry

        tk.Button(nova_janela, text="Cadastrar", bg="#4CAF50", fg="#ffffff", font=("Helvetica", 12),
                  command=lambda: Sistema.cadastrar_coletor(self, nova_janela, entries)).place(x=150, y=220)

    @staticmethod
    def abrir_janela_cadastro_coordenador(self):
        nova_janela = tk.Toplevel()
        nova_janela.title("Cadastro de Gestor")
        Sistema.centralizar_janela(nova_janela, 400, 400)
        nova_janela.configure(bg="#f0f0f0")

        entries = {}
        campos = ["username", "password", "cpf", "email", "nome", "telefone"]
        y_positions = [30, 60, 90, 120, 150, 180]

        for campo, y in zip(campos, y_positions):
            tk.Label(nova_janela, text=f"{campo.capitalize()}:", bg="#f0f0f0", fg="#333333", font=(
                "Helvetica", 12)).place(x=30, y=y)
            entry = tk.Entry(nova_janela, font=("Helvetica", 12),
                             show="*" if campo == "password" else None)
            entry.place(x=150, y=y)
            entries[campo] = entry

        tk.Button(nova_janela, text="Cadastrar", bg="#4CAF50", fg="#ffffff", font=("Helvetica", 12),
                  command=lambda: Sistema.cadastrar_gestor(self, nova_janela, entries)).place(x=150, y=220)

    def abrir_janela_cadastro_empresa(self):
        nova_janela = tk.Toplevel()
        nova_janela.title("Cadastro de empresa")
        Sistema.centralizar_janela(nova_janela, 400, 400)
        nova_janela.configure(bg="#f0f0f0")

        entries = {}
        campos = ["nome", "email", "cnpj", "cidade", "estado", "telefone"]
        y_positions = [30, 60, 90, 120, 150, 180]

        for campo, y in zip(campos, y_positions):
            tk.Label(nova_janela, text=f"{campo.capitalize()}:", bg="#f0f0f0", fg="#333333", font=(
                "Helvetica", 12)).place(x=30, y=y)
            entry = tk.Entry(nova_janela, font=("Helvetica", 12),
                             show="*" if campo == "password" else None)
            entry.place(x=150, y=y)
            entries[campo] = entry

        tk.Button(nova_janela, text="Cadastrar", bg="#4CAF50", fg="#ffffff", font=("Helvetica", 12),
                  command=lambda: Sistema.cadastrar_empresa(self, nova_janela, entries)).place(x=150, y=220)

    @staticmethod
    def abrir_janela_criar_tarefa(self):
        nova_janela = tk.Toplevel()
        nova_janela.title("Criação de tarefa")
        Sistema.centralizar_janela(nova_janela, 400, 400)
        nova_janela.configure(bg="#f0f0f0")

        entries = {}
        campos = ["descricao", "data", "hora", "local", "coletor_id"]
        y_positions = [30, 60, 90, 120, 150]

        for campo, y in zip(campos, y_positions):
            tk.Label(nova_janela, text=f"{campo.capitalize()}:", bg="#f0f0f0", fg="#333333", font=(
                "Helvetica", 12)).place(x=30, y=y)
            entry = tk.Entry(nova_janela, font=("Helvetica", 12),
                             show="*" if campo == "password" else None)
            entry.place(x=150, y=y)
            entries[campo] = entry

        tk.Button(nova_janela, text="Cadastrar", bg="#4CAF50", fg="#ffffff", font=("Helvetica", 12),
                  command=lambda: Sistema.criar_tarefa(self, nova_janela, entries)).place(x=150, y=220)

    @staticmethod
    def criar_tarefa(self, nova_janela, entries):
        descricao = entries['descricao'].get()
        data = entries['data'].get()
        hora = entries['hora'].get()
        local = entries['local'].get()
        coletor_id = entries['coletor_id'].get()

        if all([descricao, data, hora, local, coletor_id]):
            self.conn.execute("INSERT INTO tarefa (descricao, data, hora, local, coletor_id) VALUES (?, ?, ?, ?, ?)",
                              (descricao, data, hora, local, coletor_id))
            self.conn.commit()
            messagebox.showinfo("Cadastro", "Tarefa cadastrada com sucesso!")
            nova_janela.destroy()
        else:
            messagebox.showerror(
                "Cadastro", "Por favor, preencha todos os campos.")

    @staticmethod
    def cadastrar_coletor(self, nova_janela, entries):
        username = entries['username'].get()
        password = entries['password'].get()
        cpf = entries['cpf'].get()
        email = entries['email'].get()
        nome = entries['nome'].get()
        telefone = entries['telefone'].get()

        if all([username, password, cpf, email, nome, telefone]):
            self.conn.execute("INSERT INTO coletor (username, password, cpf, email, nome, telefone) VALUES (?, ?, ?, ?, ?, ?)",
                              (username, password, cpf, email, nome, telefone))
            self.conn.commit()
            messagebox.showinfo("Cadastro", "Coletor cadastrado com sucesso!")
            nova_janela.destroy()
        else:
            messagebox.showerror(
                "Cadastro", "Por favor, preencha todos os campos.")

    @staticmethod
    def cadastrar_empresa(self, nova_janela, entries):
        nome = entries['nome'].get()
        email = entries['email'].get()
        cnpj = entries['cnpj'].get()
        cidade = entries['cidade'].get()
        estado = entries['estado'].get()
        telefone = entries['telefone'].get()

        if all([nome, email, cnpj, cidade, estado, telefone]):
            self.conn.execute("INSERT INTO empresa  (nome, email, cnpj, cidade, estado, telefone) VALUES (?, ?, ?, ?, ?, ?)",
                              (nome, email, cnpj, cidade, estado, telefone))
            self.conn.commit()
            messagebox.showinfo("Cadastro", "Empresa cadastrada com sucesso!")
            nova_janela.destroy()
        else:
            messagebox.showerror(
                "Cadastro", "Por favor, preencha todos os campos.")

    @staticmethod
    def cadastrar_gestor(self, nova_janela, entries):
        username = entries['username'].get()
        password = entries['password'].get()
        cpf = entries['cpf'].get()
        email = entries['email'].get()
        nome = entries['nome'].get()
        telefone = entries['telefone'].get()

        if all([username, password, cpf, email, nome, telefone]):
            self.conn.execute("INSERT INTO gestor  (username, password, cpf, email, nome, telefone) VALUES (?, ?, ?, ?, ?, ?)",
                              (username, password, cpf, email, nome, telefone))
            self.conn.commit()
            messagebox.showinfo("Cadastro", "Gestor cadastrado com sucesso!")
            nova_janela.destroy()
        else:
            messagebox.showerror(
                "Cadastro", "Por favor, preencha todos os campos.")

    def cadastrar_usuario(self, nova_janela, entries, tipo_var):
        username = entries['username'].get()
        password = entries['password'].get()
        cpf = entries['cpf'].get()
        email = entries['email'].get()
        nome = entries['nome'].get()
        telefone = entries['telefone'].get()
        tipo = tipo_var.get()
        tipo = tipo.lower()

        if all([username, password, cpf, email, nome, telefone, tipo]):
            self.conn.execute(f"INSERT INTO {tipo} (username, password, cpf, email, nome, telefone) VALUES (?, ?, ?, ?, ?, ?)",
                              (username, password, cpf, email, nome, telefone))
            self.conn.commit()
            messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
            nova_janela.destroy()
        else:
            messagebox.showerror(
                "Cadastro", "Por favor, preencha todos os campos.")


def encerrar_aplicacao():
    root.destroy()


if __name__ == "__main__":  # incializar o sistema.
    root = tk.Tk()
    sistema = Sistema(root)
    # Associando a função de encerramento à ação de fechar a janela
    root.protocol("WM_DELETE_WINDOW", encerrar_aplicacao)
    root.mainloop()
