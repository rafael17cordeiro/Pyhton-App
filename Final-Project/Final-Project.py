
import math
from tkinter import messagebox
import sqlite3
from tkinter import ttk
import tkinter as tk
import random


class funcs():

    def adicionar_pontos(self, username, pontos):
        self.conecta_bd()
        self.cursor.execute("UPDATE Pontuacoes SET pontuacao = pontuacao + ? WHERE ut_username = ?", (pontos, username))
        self.conn.commit()
        self.desconecta_bd()
    def mostrar_pontos(self):
        self.conecta_bd()
        self.cursor.execute("SELECT pontuacao FROM Pontuacoes WHERE ut_username=?", (self.username,))
        result = self.cursor.fetchone()
        self.desconecta_bd()

        if result is not None:
            pontos = result[0]
        else:
            pontos = 0

        return pontos

    def register_user(self):
        self.conecta_bd()
        username = self.input_username.get()
        email = self.input_email.get()
        password = self.input_password.get()

        if not username or not email or not password:
            tk.messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        else:
            self.cursor.execute("SELECT * FROM Utilizadores WHERE username=? OR email=?", (username, email))
            existing_user = self.cursor.fetchone()

            if existing_user:
                tk.messagebox.showerror("Erro", "Nome de Utilizador ou e-mail já existem.")
                tk.messagebox.showerror("Erro", "Caso já tenha conta registada clique em Login")
            else:
                self.cursor.execute("INSERT INTO Utilizadores (username, email, password) VALUES (?, ?, ?)",
                                    (username, email, password))
                self.conn.commit()
                tk.messagebox.showinfo("Registo", "Registado com sucesso !")
                self.cursor.execute("SELECT id FROM Utilizadores WHERE username=?", (username,))
                user_id = self.cursor.fetchone()[0]

                self.cursor.execute("INSERT INTO Pontuacoes (ut_username, pontuacao) VALUES (?, ?)",
                                    (username, 0))
                self.conn.commit()
        self.desconecta_bd()

    def login_user(self):
            self.conecta_bd()
            username = self.input_username.get()
            password = self.input_password.get()

            self.cursor.execute("SELECT * FROM Utilizadores WHERE username=? AND password=?", (username, password))
            existing_user = self.cursor.fetchone()

            if existing_user:
                if username == "Admin" and password == "6969":
                    self.root.destroy(),
                    self.abrir_admin(username)
                else:
                    tk.messagebox.showinfo("Login", "Login com sucesso !")
                    self.abrir_segunda_janela(username)
                    self.root.destroy()
            else:
                tk.messagebox.showerror("Erro", "Dados inseridos inválidos!")

            self.desconecta_bd()

    def abrir_Login(self):
        self.root.destroy(),
        root = tk.Tk()
        Application(root)
    def abrir_segunda_janela(self,username):
        root2 = tk.Tk()
        Application2(root2,username )

    def abrir_gamemaster(self,username):
        self.root.destroy(),
        root3 = tk.Tk()
        Application3(root3,username)

    def abrir_admin(self,username):
        root4= tk.Tk()
        Application4(root4, username)
        print("Administrator ON!")

    def abrir_profile(self,username):
        root5 = tk.Tk()
        profile_app = Application5(root5, username)
        email = self.obter_email(username)
        user_id = self.obter_id(username)
        profile_app.mostrar_informacoes(username, email, user_id)

    def obter_email(self, username):
        self.conecta_bd()
        self.cursor.execute("SELECT email FROM Utilizadores WHERE username=?", (username,))
        result = self.cursor.fetchone()
        self.desconecta_bd()

        return result[0] if result else None

    def obter_id(self, username):
        self.conecta_bd()
        self.cursor.execute("SELECT id FROM Utilizadores WHERE username=?", (username,))
        result = self.cursor.fetchone()
        self.desconecta_bd()

        return result[0] if result else None
    def conecta_bd(self):
        self.conn = sqlite3.connect('hub_jogos.db')
        self.cursor = self.conn.cursor()
        print("Ligado à base de dados")

    def desconecta_bd(self):
        self.conn.close()
        print("Desligar a base de dados")

    def lista_frame2(self):


        self.listaCli = ttk.Treeview(self.root, height=1, column=("col1", "col2", "col3", "col4"))
        self.listaCli.heading("#0", text="", anchor=tk.W)
        self.listaCli.heading("#1", text="Lugar")
        self.listaCli.heading("#2", text="ID")
        self.listaCli.heading("#3", text="Username")
        self.listaCli.heading("#4", text="Pontos")

        self.listaCli.column("#0", width=0, stretch=tk.NO)
        self.listaCli.column("#1", width=10)
        self.listaCli.column("#2", width=10)
        self.listaCli.column("#3", width=10)
        self.listaCli.column("#4", width=10)


        self.listaCli.place(relx=0.05       , rely=0.13, relwidth=0.38, relheight=0.78)

    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(
            "SELECT Utilizadores.id, Utilizadores.username, Pontuacoes.pontuacao "
            "FROM Utilizadores "
            "INNER JOIN Pontuacoes ON Utilizadores.username = Pontuacoes.ut_username "
            "ORDER BY Pontuacoes.pontuacao DESC;"
        )

        # Counter for row number
        row_num = 1

        for item in lista:
            self.listaCli.insert("", "end", values=(row_num, item[0], item[1], item[2]))
            row_num += 1

        self.desconecta_bd()




    def tela(self):
        self.root.title("GamesMaster INC.")
        self.root.configure(background="#101e29")
        self.root.resizable(False, False)
    def center_window1(self):
        window_width = 400
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = math.floor((screen_width - window_width) / 2)
        y = math.floor((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def center_window2(self):
            window_width = 1100
            window_height = 600
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = math.floor((screen_width - window_width) / 2)
            y = math.floor((screen_height - window_height) / 2)
            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def center_window3(self):
        window_width = 700
        window_height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = math.floor((screen_width - window_width) / 2)
        y = math.floor((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def center_window4(self):
        window_width = 900
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = math.floor((screen_width - window_width) / 2)
        y = math.floor((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def center_window5(self):
        window_width = 400
        window_height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = math.floor((screen_width - window_width) / 2)
        y = math.floor((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")




class funcsAdmin():


    def listaAdmin(self):
        self.listaCli = ttk.Treeview(self.root, height=1, column=("col1", "col2", "col3", "col4","col5",))
        self.listaCli.heading("#0", text="", anchor=tk.W)
        self.listaCli.heading("#1", text="Lugar")
        self.listaCli.heading("#2", text="ID")
        self.listaCli.heading("#3", text="Username")
        self.listaCli.heading("#4", text="Email")
        self.listaCli.heading("#5", text="Pontos")

        self.listaCli.column("#0", width=0, stretch=tk.NO)
        self.listaCli.column("#1", width=10)
        self.listaCli.column("#2", width=10)
        self.listaCli.column("#3", width=10)
        self.listaCli.column("#4", width=10)
        self.listaCli.column("#5", width=10)

        self.listaCli.place(relx=0.02, rely=0.13, relwidth=0.65, relheight=0.71 )

    def selectlistaAdmin(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(
            "SELECT Utilizadores.id, Utilizadores.username, Utilizadores.email, Pontuacoes.pontuacao "
            "FROM Utilizadores "
            "INNER JOIN Pontuacoes ON Utilizadores.username = Pontuacoes.ut_username "
            "ORDER BY Pontuacoes.pontuacao DESC;"
        )


        row_num = 1

        for item in lista:
            self.listaCli.insert("", "end", values=(row_num, item[0], item[1], item[2], item[3]))
            row_num += 1

        self.desconecta_bd()

    def procurar(self, utInput, listaCli):
        username = utInput.get()

        if not username:
            messagebox.showinfo("Aviso", "Preencha o campo do username")
            return

        self.conecta_bd()
        listaCli.delete(*listaCli.get_children())

        lista = self.cursor.execute(
            "SELECT Utilizadores.id, Utilizadores.username, Utilizadores.email, Pontuacoes.pontuacao "
            "FROM Utilizadores "
            "INNER JOIN Pontuacoes ON Utilizadores.username = Pontuacoes.ut_username "
            "WHERE Utilizadores.username LIKE ? "
            "ORDER BY Pontuacoes.pontuacao DESC;",
            ('%' + username + '%',)
        )

        rows = lista.fetchall()
        if not rows:
            messagebox.showinfo("Aviso", "Utilizador não encontrado")
        else:
            row_num = 1
            for item in rows:
                listaCli.insert("", "end", values=(row_num, item[0], item[1], item[2], item[3]))
                row_num += 1

        self.desconecta_bd()

    def eliminar(self, idInput, utInput, listaCli):
        user_id = idInput.get()
        username = utInput.get()

        if not user_id or not username:
            messagebox.showinfo("Aviso", "Preencha o ID e o username")
            return

        self.conecta_bd()
        self.cursor.execute("SELECT * FROM Utilizadores WHERE id = ? AND username = ?", (user_id, username))
        user_exists = self.cursor.fetchone()

        if user_exists:
            # Excluir o usuário da tabela de pontuações
            self.cursor.execute("DELETE FROM Pontuacoes WHERE ut_username = ?", (username,))
            self.conn.commit()

            # Excluir o usuário da tabela de Utilizadores
            self.cursor.execute("DELETE FROM Utilizadores WHERE id = ?", (user_id,))
            self.conn.commit()

            listaCli.delete(*listaCli.get_children())
            self.selectlistaAdmin()

            messagebox.showinfo("Sucesso", "Registros eliminados com sucesso!")
        else:
            messagebox.showinfo("Aviso", "Utilizador não encontrado")

        self.desconecta_bd()

    def inserir(self, utInput, emailInput, passInput, listaCli):
        username = utInput.get()
        email = emailInput.get()
        password = passInput.get()

        if not username or not email or not password:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return
        self.conecta_bd()
        self.cursor.execute("SELECT * FROM Utilizadores WHERE username=? OR email=?", (username, email))
        existing_user = self.cursor.fetchone()

        if existing_user:
            messagebox.showerror("Erro", "Nome de Utilizador ou e-mail já existem.")
            self.desconecta_bd()
            return
        else:

            self.cursor.execute("INSERT INTO Utilizadores (username, email, password) VALUES (?, ?, ?)",
                                (username, email, password))
            self.conn.commit()
            messagebox.showinfo("Registo", "Registado com sucesso!")


            self.cursor.execute("SELECT id FROM Utilizadores WHERE username=?", (username,))
            user_id = self.cursor.fetchone()[0]


            self.cursor.execute("INSERT INTO Pontuacoes (ut_username, pontuacao) VALUES (?, ?)",
                                (username, 0))
            self.conn.commit()
            self.selectlistaAdmin()

            self.desconecta_bd()

    def update(self, idInput, utInput, emailInput, passInput):
        user_id = idInput.get()
        novo_username = utInput.get()
        novo_email = emailInput.get()
        nova_password = passInput.get()

        # Verifica se foi fornecido o ID
        if not user_id:
            messagebox.showerror("Erro", "Preencha o ID")
            return

        self.conecta_bd()

        # Verifica se o ID existe na base de dados
        consulta_verificacao = "SELECT id FROM Utilizadores WHERE id = ?"
        resultado = self.cursor.execute(consulta_verificacao, (user_id,))
        usuario_existente = resultado.fetchone()

        if usuario_existente:
            consulta_verifica_username = "SELECT username FROM Utilizadores WHERE id = ?"
            resultado_username = self.cursor.execute(consulta_verifica_username, (user_id,))
            username_atual = resultado_username.fetchone()

            if username_atual[0] != novo_username:
                consulta_update = "UPDATE Utilizadores SET username = ?, email = ?, password = ? WHERE id = ?"
                self.cursor.execute(consulta_update, (novo_username, novo_email, nova_password, user_id))
                self.conn.commit()

                # Atualiza o nome de usuário na tabela Pontuacoes
                consulta_update_pontuacoes = "UPDATE Pontuacoes SET ut_username = ? WHERE ut_username = ?"
                self.cursor.execute(consulta_update_pontuacoes, (novo_username, username_atual[0]))
                self.conn.commit()

                self.selectlistaAdmin()
                messagebox.showinfo("Update", "Utilizador atualizado")
            else:
                # Se o username não foi alterado, atualiza apenas os campos na tabela Utilizadores
                consulta_update = "UPDATE Utilizadores SET email = ?, password = ? WHERE id = ?"
                self.cursor.execute(consulta_update, (novo_email, nova_password, user_id))
                self.conn.commit()

                self.selectlistaAdmin()
                messagebox.showinfo("Update", "Utilizador atualizado")
        else:
            messagebox.showerror("Erro", "Utilizador não encontrado")

        self.desconecta_bd()


class Application5(funcs):
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.tela()
        self.center_window5()
        print(username)

        self.profile = tk.Label(self.root, text="Profile👤", bg="#101e29", fg="white", font=("Nunito", 24, "bold"))
        self.profile.place(relx=0.15, rely=0.08, relwidth=0.7, relheight=0.1)

        self.voltar = tk.Button(
            self.root,
            text="Fechar",
            bg="#0099ff",
            fg="white",
            activebackground="#0099ff",
            activeforeground="white",
            font=("Nunito", 11, "bold"),
            bd=0,
            command=lambda: self.root.destroy()
        )
        self.voltar.place(relx=0.26, rely=0.8, relwidth=0.5, relheight=0.1)  # Ajuste vertical para criar mais espaço
    def mostrar_informacoes(self, username, email, user_id):
            self.UsernameLabel = tk.Label(self.root, text=f"Username: {username}", bg="#101e29", fg="white",
                                          font=("Nunito", 14, "bold"))
            self.UsernameLabel.place(relx=0.05, rely=0.325)



            self.emailLabel = tk.Label(self.root, text=f"Email: {email}", bg="#101e29", fg="white",
                                       font=("Nunito", 14, "bold"))
            self.emailLabel.place(relx=0.05, rely=0.425)

            self.idLabel = tk.Label(self.root, text=f"ID: {user_id}", bg="#101e29", fg="white",
                                    font=("Nunito", 14, "bold"))
            self.idLabel.place(relx=0.05, rely=0.525)



class Application4(funcs, funcsAdmin):
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.tela()
        self.center_window4()
        self.elements4()
        self.listaAdmin()
        self.selectlistaAdmin()
    def elements4(self):
        self.btnVoltar = tk.Button(
            self.root,
            text="⬅️",
            bg="tomato",
            fg="#101e29",
            activebackground="tomato",
            activeforeground="#101e29",
            font=("Nunito", 24),
            bd=0,
            command=self.abrir_Login,

        )
        self.btnVoltar.place(relx=0.94, rely=0.02,  relwidth=0.035, relheight=0.0511)

        self.AdminLabel = tk.Label(text="Admin Menu", bg="#101e29", fg="white", font=("Nunito", 24, "bold"))
        self.AdminLabel.place(relx=0.33, rely=0, relwidth=0.29, relheight=0.09)

        self.adminIcon = tk.Label(text="🛠", bg="#101e29", fg="white", font=("Nunito", 24))
        self.adminIcon.place(relx=0.59, rely=0, relwidth=0.04, relheight=0.07)

        self.idLabel = tk.Label(self.root, text="Id", bg="#101e29", fg="white", font=("Nunito", 12, "bold"))
        self.idLabel.place(relx=0.68, rely=0.12, relwidth=0.1, relheight=0.05)

        self.idInput = tk.Entry(self.root, font=("Nunito", 10))
        self.idInput.place(relx=0.78, rely=0.13, relwidth=0.2, relheight=0.03)

        self.utLabel = tk.Label(self.root, text="Username", bg="#101e29",fg="white", font=("Nunito", 12, "bold"))
        self.utLabel.place(relx=0.68, rely=0.18, relwidth=0.1, relheight=0.05)

        self.utInput = tk.Entry(self.root, font=("Nunito", 10))
        self.utInput.place(relx=0.78, rely=0.19, relwidth=0.2, relheight=0.03)


        self.emailLabel = tk.Label(self.root, text="Email", bg="#101e29", fg="white", font=("Nunito", 12, "bold"))
        self.emailLabel.place(relx=0.68, rely=0.24, relwidth=0.1, relheight=0.05)

        self.emailInput = tk.Entry(self.root, font=("Nunito", 10))
        self.emailInput.place(relx=0.78, rely=0.25, relwidth=0.2, relheight=0.03)


        self.passlabel = tk.Label(self.root, text="Password", bg="#101e29", fg="white", font=("Nunito", 12, "bold"))
        self.passlabel.place(relx=0.68, rely=0.3, relwidth=0.1, relheight=0.05)

        self.passInput = tk.Entry(self.root, font=("Nunito", 10))
        self.passInput.place(relx=0.78, rely=0.31, relwidth=0.2, relheight=0.03)


        self.btnInsert = tk.Button(
            self.root,
            text="Inserir ➕", bg="#162938",bd=0, fg="white", font=("Nunito", 11, "bold"),
            command=lambda: self.inserir(self.utInput, self.emailInput, self.passInput, self.listaCli),
            cursor='hand2'
        )
        self.btnInsert.place(relx=0.685, rely=0.40, relwidth=0.3, relheight=0.08)

        self.btnDelete = tk.Button(
            self.root,
            text="Eliminar 🗑️", bg="#162938", bd=0, fg="white", font=("Nunito", 11, "bold"),
            command=lambda: self.eliminar(self.idInput,self.utInput, self.listaCli),
            cursor='hand2'
        )
        self.btnDelete.place(relx=0.685, rely=0.49, relwidth=0.3, relheight=0.08)



        self.btnShow = tk.Button(
            self.root,
            text="Mostrar todos 👁️", bg="#162938", fg="white",bd=0, font=("Nunito", 11, "bold"),
            command=self.selectlistaAdmin,
            cursor='hand2'
        )
        self.btnShow.place(relx=0.685, rely=0.58, relwidth=0.3, relheight=0.08)

        # butao para pesquisar
        self.btnSearch = tk.Button(
            self.root,
            text="Procurar 🔎", bg="#162938", fg="white",bd=0, font=("Nunito", 11, "bold"),
            command=lambda: self.procurar(self.utInput, self.listaCli),
            cursor='hand2'
        )
        self.btnSearch.place(relx=0.685, rely=0.67, relwidth=0.3, relheight=0.08)

        self.btnUpdate = tk.Button(
            self.root,
            text="Update ♻️", bg="#162938", fg="white", bd=0, font=("Nunito", 11, "bold"),
            command=lambda: self.update(self.idInput, self.utInput, self.emailInput, self.passInput),
            cursor='hand2'
        )
        self.btnUpdate.place(relx=0.685, rely=0.76, relwidth=0.3, relheight=0.08)


class Application3(funcs):
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.center_window3()
        self.tela()
        self.elements3()
        print(username)


    def elements3(self):

        self.btn3 = tk.Button(
            self.root,
            text="Guess",
            bg="#162938",
            fg="white",
            font=("Nunito", 11, "bold"),
            bd=0,
            command=lambda: self.guess_game(),
            cursor='hand2'

        )
        self.btn3.place(relx=0.35, rely=0.55, relwidth=0.3, relheight=0.15)

        self.text = tk.Label(
            self.root,
            text="Advinha o numero entre 1 e 10!",
            bg="#101e29",
            fg="white",
            font=("Nunito", 18, "bold"),
            justify="center"
        )
        self.text.place(relx=0.0, rely=0.15, relwidth=1, relheight=0.2)

        self.btnVoltar = tk.Button(
            self.root,
            text="⬅️",
            bg="tomato",
            fg="#101e29",
            font=("Nunito", 24),
            bd=0,
            command=lambda: [self.root.destroy(), self.abrir_segunda_janela(self.username)],
            cursor='hand2'
        )
        self.btnVoltar.place(relx=0.94, rely=0.025, relwidth=0.040, relheight=0.09)

        self.icon1 = tk.Label(
            self.root,
            text="👾",
            bg="#101e29",
            fg="#0099ff",
            font=("Nunito", 30),
            justify="center"
        )
        self.icon1.place(relx=0.17, rely=0.15, relwidth=0.05, relheight=0.15)

        self.icon2 = tk.Label(
            self.root,
                text="👾",
            bg="#101e29",
            fg="#0099ff",
            font=("Nunito", 30),
            justify="center"
        )
        self.icon2.place(relx=0.78, rely=0.15, relwidth=0.05, relheight=0.15)

        self.input_guess = tk.Entry(self.root, font=("Nunito", 13,))
        self.input_guess.place(relx=0.3, rely=0.35, relwidth=0.40, relheight=0.1)

    def guess_game(self):
        try:
            guess = int(self.input_guess.get())

            if 1 <= guess <= 10:
                random_number = random.randint(1, 10)
                if guess == random_number:
                    messagebox.showinfo("Parabéns!", "Acertaste no número!")
                    self.adicionar_pontos(self.username, 100)
                    self.root.destroy()
                    self.abrir_segunda_janela(self.username)
                else:
                    messagebox.showinfo("Falhaste :(", f"Tenta de novo, o número correto era {random_number}")
            else:
                messagebox.showwarning("Dados inválidos", "Insere um número de 1 a 10!")
        except ValueError:
            messagebox.showwarning("Dados inválidos", "Insere um número válido!")


class Application2(funcs):
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.center_window2()
        self.tela()
        self.elements2()
        self.lista_frame2()
        self.select_lista()
        self.frames_da_tela()
        print(username)
    def elements2(self):
        self.btnProfile = tk.Button(
            self.root,
            text="👤",
            bg="#101e29",
            fg="white",
            activebackground="#101e29",
            activeforeground="white",
            font=("Nunito", 32),
            bd=0,
            command=lambda: self.abrir_profile(self.username),
            cursor='hand2'

        )
        self.btnProfile.place(relx=0.87, rely=0.04, relwidth=0.035, relheight=0.065)
        self.btnVoltar = tk.Button(
            self.root,
            text="⬅️",
            bg = "tomato",
            fg = "#101e29",
            activebackground="tomato",  # Cor do fundo quando clicado
            activeforeground="#101e29",  # Cor do texto quando clicado
            font = ("Nunito", 24),
            bd=0,
            command=self.abrir_Login,
            cursor = 'hand2'
        )
        self.btnVoltar.place(relx=0.91, rely=0.05, relwidth=0.027, relheight=0.0511)



        self.btn2 = tk.Button(
            self.root,
            text="Play",
            bg="#2E8B57",
            fg="white",
            activebackground="#2E8B57",  # Cor do fundo quando clicado
            activeforeground="white",  # Cor do texto quando clicado
            font=("Nunito", 11, "bold"),
            bd=0,
            command=lambda: self.abrir_gamemaster(self.username),
            cursor='hand2'
        )
        self.btn2.place(relx=0.585, rely=0.825, relwidth=0.25, relheight=0.07)



        self.text = tk.Label(self.root,
                             text="Este é um jogo simples onde tens de adivinhar um número entre\n"
                                  "                         1 e 10. Se acertares, ganhas 100 pontos",
                             bg="#101e29", fg="white", font=("Nunito", 12, "bold"), justify="left")
        self.text.place(relx=0.38, rely=0.7, relwidth=0.65, relheight=0.1)

        pontos = self.mostrar_pontos()

        self.pontos = tk.Label(self.root,
                               text=f"Pontos: {pontos}",
                               bg="#101e29", fg="white",
                               font=("Nunito", 14, "bold"))
        self.pontos.place(relx=0.43, rely=0.05, relwidth=0.2, relheight=0.05)


        self.iconPontos = tk.Label(
            self.root,
            text="💎",
            bg="#101e29",
            fg="#0099ff",
            font=("Nunito", 24),
            justify="center"
        )
        self.iconPontos.place(relx=0.58, rely=0.028, relwidth=0.05, relheight=0.08)






        self.leaderboard = tk.Label(self.root,text="LeaderBoard", bg="#101e29", fg="white", font=("Nunito", 32, "bold"))
        self.leaderboard.place(relx=0.05, rely=0.015, relwidth=0.35, relheight=0.1)

        self.iconCrown = tk.Label(
            self.root,
            text="👑",
            bg="#101e29",
            fg="#F7E300",
            font=("Nunito", 34, ""),
            justify="center"
        )
        self.iconCrown.place(relx=0.35, rely=0.013 , relwidth=0.05, relheight=0.09)


    def frames_da_tela(self):
        self.frame_1 = tk.Frame(self.root, bd=4, bg='#162938', highlightbackground='white', highlightthickness=2)
        self.frame_1.place(relx=0.48, rely=0.13, relwidth=0.46, relheight=0.56)






class Application(funcs):
    def __init__(self, root):
        self.root = root
        self.center_window1()
        self.tela()
        self.elements()


    def elements(self):
        self.logo = tk.Label(text="GameMaster Inc", bg="#101e29", fg="white", font=("Nunito", 24, "bold"))
        self.logo.place(relx=0.15, rely=0.04, relwidth=0.7, relheight=0.1)


        #username
        self.username = tk.Label(text="Username 👤", bg="#101e29", fg="white", font=("Nunito", 14,))
        self.username.place(relx=0.04, rely=0.25, relwidth=0.5, relheight=0.1)

        self.input_username =tk.Entry(self.root ,font=("Nunito", 9,))
        self.input_username.place(relx=0.15, rely=0.35, relwidth=0.70, relheight=0.05)

        # email
        self.email = tk.Label(text="Email 📩", bg="#101e29", fg="white", font=("Nunito", 14,))
        self.email.place(relx=0.044, rely=0.40, relwidth=0.4, relheight=0.1)

        self.input_email =tk.Entry(self.root ,font=("Nunito", 9,))
        self.input_email.place(relx=0.15, rely=0.50, relwidth=0.70, relheight=0.05)


        #password
        self.password = tk.Label(text="Password 🔑", bg="#101e29", fg="white", font=("Nunito", 14,))
        self.password.place(relx=0.04, rely=0.55, relwidth=0.5, relheight=0.1)

        self.input_password = tk.Entry(self.root, font=("Nunito", 12,), show="•")

        self.input_password.place(relx=0.15, rely=0.65, relwidth=0.70, relheight=0.05)

        self.btn2 = tk.Button(text="Register", bg="#162938",bd=0, fg="white", font=("Nunito", 11, "bold"),
                              command=self.register_user,cursor='hand2')
        self.btn2.place(relx=0.15, rely=0.8, relwidth=0.3, relheight=0.10)

        self.btn1 = tk.Button(text="Login", bg="#162938", fg="white",bd=0, font=("Nunito", 11, "bold"), command=self.login_user,
            cursor='hand2')
        self.btn1.place(relx=0.55, rely=0.8, relwidth=0.3, relheight=0.10)




root = tk.Tk()
app = Application(root)
root.mainloop()