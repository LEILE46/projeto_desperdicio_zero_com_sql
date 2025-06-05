from tkinter import *
from tkinter import messagebox
from servico.usuario_servico import cadastrar_usuario, buscar_usuario_por_email
from servico.alimentos_servicos import cadastrar_alimento, listar_alimentos_disponiveis
from servico.retirada_servico import marcar_retirada, listar_retiradas_do_usuario
from servico.avaliacao_servico import avaliar_usuario

usuario_logado = None
menu_global = None
def criar_campos_login(janela):
    """Criação dos campos para login/cadastro"""
    Label(janela, text="Nome:", bg="#e6f2ff", fg="#003366", font=("Arial", 12)).pack(anchor="w", padx=40)
    nome_entry = Entry(janela, font=("Arial", 12))
    nome_entry.pack(padx=40, pady=5)

    Label(janela, text="Email:", bg="#e6f2ff", fg="#003366", font=("Arial", 12)).pack(anchor="w", padx=40)
    email_entry = Entry(janela, font=("Arial", 12))
    email_entry.pack(padx=40, pady=5)

    Label(janela, text="Localização:", bg="#e6f2ff", fg="#003366", font=("Arial", 12)).pack(anchor="w", padx=40)
    local_entry = Entry(janela, font=("Arial", 12))
    local_entry.pack(padx=40, pady=5)

    Label(janela, text="Tipo de perfil (pessoa ou ong):", bg="#e6f2ff", fg="#003366", font=("Arial", 12)).pack(anchor="w", padx=40)
    tipo_entry = Entry(janela, font=("Arial", 12))
    tipo_entry.pack(padx=40, pady=5)

    return nome_entry, email_entry, local_entry, tipo_entry
def iniciar_interface():
    janela = Tk()
    janela.title("Doação e Resgate de Alimentos - Não Desperdice!")
    janela.geometry("460x480")
    janela.configure(bg="#e6f2ff")

    Label(janela, text="Bem-vindo ao app desperdício zero com doações inclusas", font=("Helvetica", 16, "bold"),
          bg="#e6f2ff", fg="#004080").pack(pady=20)

    # Campos de login/cadastro
    nome_entry, email_entry, local_entry, tipo_entry = criar_campos_login(janela)

    # Botões de ação
    Button(janela, text="Cadastrar", bg="#007acc", fg="white", font=("Arial", 13, "bold"),
           command=lambda: fazer_cadastro(nome_entry, email_entry, tipo_entry, local_entry)).pack(pady=10, ipadx=20, ipady=5)
    Button(janela, text="Login", bg="#005c99", fg="white", font=("Arial", 13, "bold"),
           command=lambda: fazer_login(email_entry, janela)).pack(pady=10, ipadx=20, ipady=5)

    janela.mainloop()

    def fazer_cadastro(nome_entry, email_entry, tipo_entry, local_entry):
        """Função de cadastro de usuário"""
        nome = nome_entry.get().strip()
        email = email_entry.get().strip()
        tipo = tipo_entry.get().strip().lower()
        local = local_entry.get().strip()

        if not nome or not email or not tipo or not local:
            messagebox.showwarning("Campos incompletos", "Por favor, preencha todos os campos.")
            return
        if tipo not in ("pessoa", "ong"):
            messagebox.showwarning("Tipo inválido", "Digite 'pessoa' ou 'ong' para o tipo de perfil.")
            return
        if buscar_usuario_por_email(email):
            messagebox.showwarning("Email já cadastrado", "Este email já foi registrado. Faça login.")
            return

    
        cadastrar_usuario(nome, email, tipo, local)
        messagebox.showinfo("Cadastro realizado", f"Olá {nome}! Cadastro efetuado com sucesso.")

    def fazer_login(email_entry, janela):
        """Função de login de usuário"""
        email = email_entry.get().strip()
        usuario = buscar_usuario_por_email(email)
        if usuario:
            global usuario_logado
            usuario_logado = usuario
            print(f"Login bem-sucedido: {usuario_logado.nome}, {usuario_logado.tipo_perfil}")
            janela.destroy()  # Fechar a tela de login
            abrir_menu_principal()  # Abrir o menu principal
        else:
            messagebox.showerror("Usuário não encontrado", "Email não cadastrado. Faça o cadastro primeiro.")

    def abrir_menu_principal():
        """Função que abre o menu principal após o login"""
        global menu_global
        menu = Tk()
        menu_global = menu  # Variável global para menu
        menu.title("Menu Principal - Doação de Alimentos")
        menu.geometry("920x520")
        menu.configure(bg="#f0f8ff")  # alice blue

        Label(menu, text=f"Olá, {usuario_logado.nome} ({usuario_logado.tipo_perfil.upper()})",
            font=("Helvetica", 16, "bold"), bg="#f0f8ff", fg="#004080").pack(pady=15)
        print("Usuário logado:", usuario_logado.nome, usuario_logado.tipo_perfil)

        # Botões do menu principal
        criar_botao_menu(menu)
        menu.mainloop()



    def tela_cadastro_alimento():
        top = Toplevel()
        top.title("Cadastrar Alimento")
        top.geometry("400x320")
        top.configure(bg="#f7f9fc")

        Label(top, text="Nome do alimento:", bg="#f7f9fc", fg="#003366", font=("Arial", 12)).pack(anchor="w", padx=25, pady=8)
        nome_entry = Entry(top, font=("Arial", 12))
        nome_entry.pack(padx=25)

        Label(top, text="Validade (AAAA-MM-DD):", bg="#f7f9fc", fg="#003366", font=("Arial", 12)).pack(anchor="w", padx=25, pady=8)
        validade_entry = Entry(top, font=("Arial", 12))
        validade_entry.pack(padx=25)

        Label(top, text="Quantidade:", bg="#f7f9fc", fg="#003366", font=("Arial", 12)).pack(anchor="w", padx=25, pady=8)
        quantidade_entry = Entry(top, font=("Arial", 12))
        quantidade_entry.pack(padx=25)

        def salvar():
            nome = nome_entry.get().strip()
            validade = validade_entry.get().strip()
            quantidade = quantidade_entry.get().strip()

            if not nome or not validade or not quantidade:
                messagebox.showwarning("Erro", "Preencha todos os campos.")
                return
            try:
                qtd_int = int(quantidade)
                if qtd_int <= 0:
                    raise ValueError
            except:
                messagebox.showerror("Erro", "Quantidade inválida. Use número inteiro maior que zero.")
                return

            alimento = cadastrar_alimento(nome, validade, qtd_int, usuario_logado)
            if alimento:
                messagebox.showinfo("Sucesso", "Alimento cadastrado com sucesso!")
                top.destroy()
            else:
                messagebox.showerror("Erro", "Validade inválida ou alimento vencido. Não podemos aceitar alimentos vencidos.")

        Button(top, text="Salvar", bg="#28a745", fg="white", font=("Arial", 12, "bold"), command=salvar).pack(pady=20, ipadx=30, ipady=8)
    def tela_buscar_alimentos():
        top = Toplevel()
        top.title("Alimentos Disponíveis para Retirada")
        top.geometry("450x400")
        top.configure(bg="#fffaf0")  

        alimentos = listar_alimentos_disponiveis()
        if not alimentos:
            Label(top, text="Nenhum alimento disponível no momento.", bg="#fffaf0", fg="#666", font=("Arial", 12, "italic")).pack(pady=20)
            return

        for a in alimentos:
            texto = f"{a.nome} | Validade: {a.validade} | Quantidade: {a.quantidade} | Doador ID: {a.doador_id}"
            Label(top, text=texto, bg="#fffaf0", fg="#004080", font=("Arial", 11)).pack(anchor="w", padx=15, pady=4)

    def tela_marcar_retirada():
        top = Toplevel()
        top.title("Agendar Retirada")
        top.geometry("450x400")
        top.configure(bg="#fff8dc") 

        alimentos = listar_alimentos_disponiveis()
        if not alimentos:
            Label(top, text="Nenhum alimento disponível para agendar.", bg="#fff8dc", fg="#666", font=("Arial", 12, "italic")).pack(pady=20)
            return

        lista = Listbox(top, font=("Arial", 12), selectbackground="#007acc", selectforeground="white")
        for i, a in enumerate(alimentos):
            lista.insert(i, f"{a.nome} - Validade: {a.validade} - Qtde: {a.quantidade} - Doador ID: {a.doador_id}")
        lista.pack(padx=20, pady=10, fill=BOTH, expand=True)

        Label(top, text="Data da retirada (AAAA-MM-DD):", bg="#fff8dc", fg="#003366", font=("Arial", 12)).pack(pady=5)
        data_entry = Entry(top, font=("Arial", 12))
        data_entry.pack(padx=20)

        Label(top, text="Local da retirada:", bg="#fff8dc", fg="#003366", font=("Arial", 12)).pack(pady=5)
        local_entry = Entry(top, font=("Arial", 12))
        local_entry.pack(padx=20)

        def agendar():
            index = lista.curselection()
            if not index:
                messagebox.showwarning("Seleção", "Por favor, selecione um alimento da lista.")
                return
            alimento = alimentos[index[0]]
            data = data_entry.get().strip()
            local = local_entry.get().strip()

            if not data or not local:
                messagebox.showwarning("Campos incompletos", "Informe a data e o local para retirada.")
                return

            retirada = marcar_retirada(usuario_logado, alimento, data, local)
            if retirada:
                messagebox.showinfo("Sucesso", "Retirada agendada com sucesso!")
                top.destroy()
            else:
                messagebox.showerror("Erro", "Alimento já reservado ou dados inválidos.")
        
        Button(top, text="Agendar Retirada", bg="#ff9800", fg="white", font=("Arial", 13, "bold"), command=agendar).pack(pady=15, ipadx=20, ipady=7)

    def tela_historico():
        top = Toplevel()
        top.title("Histórico de Retiradas")
        top.geometry("450x400")
        top.configure(bg="#f0fff0")

        historico = listar_retiradas_do_usuario(usuario_logado)
        if not historico:
            Label(top, text="Você não possui retiradas agendadas.", bg="#f0fff0", fg="#666", font=("Arial", 12, "italic")).pack(pady=20)
            return

        for r in historico:
        
            texto = f"{r.alimento.nome} - Data: {r.data} - Local: {r.local}" 
            Label(top, text=texto, bg="#f0fff0", fg="#004d00", font=("Arial", 12)).pack(anchor="w", padx=15, pady=5)

    def tela_avaliar():
        top = Toplevel()
        top.title("Avaliar Usuário")
        top.geometry("400x350")
        top.configure(bg="#ffe4e1") 

        Label(top, text="Email do usuário a avaliar:", bg="#ffe4e1", fg="#800000", font=("Arial", 12)).pack(anchor="w", padx=25, pady=10)
        email_entry = Entry(top, font=("Arial", 12))
        email_entry.pack(padx=25)

        Label(top, text="Nota (1 a 5):", bg="#ffe4e1", fg="#800000", font=("Arial", 12)).pack(anchor="w", padx=25, pady=10)
        nota_entry = Entry(top, font=("Arial", 12))
        nota_entry.pack(padx=25)

        Label(top, text="Comentário:", bg="#ffe4e1", fg="#800000", font=("Arial", 12)).pack(anchor="w", padx=25, pady=10)
        comentario_entry = Entry(top, font=("Arial", 12))
        comentario_entry.pack(padx=25)

        def avaliar():
            email = email_entry.get().strip()
            try:
                nota = int(nota_entry.get().strip())
                if nota < 1 or nota > 5:
                    raise ValueError
            except:
                messagebox.showerror("Nota inválida", "Informe uma nota entre 1 e 5.")
                return

            comentario = comentario_entry.get().strip()
            usuario = buscar_usuario_por_email(email)
            if not usuario:
                messagebox.showerror("Usuário não encontrado", "Email não cadastrado.")
                return

            avaliar_usuario(usuario, nota, comentario)
            messagebox.showinfo("Avaliação registrada", "Obrigado pela avaliação!")
            top.destroy()

        Button(top, text="Enviar Avaliação", bg="#9c27b0", fg="white", font=("Arial", 13, "bold"), command=avaliar).pack(pady=20, ipadx=20, ipady=7)
    def criar_botao_menu(menu):
        criar_botao_menu(menu)
        menu.mainloop()

        """Criação dos botões do menu principal"""
        Button(menu, text="Cadastrar Alimento", bg="#28a745", fg="white", font=("Arial", 13, "bold"), command=tela_cadastro_alimento).pack(pady=8, ipadx=25, ipady=7)
        Button(menu, text="Ver Alimentos Disponíveis", bg="#007bff", fg="white", font=("Arial", 13, "bold"), command=tela_buscar_alimentos).pack(pady=8, ipadx=25, ipady=7)
        Button(menu, text="Agendar Retirada", bg="#ff9800", fg="white", font=("Arial", 13, "bold"), command=tela_marcar_retirada).pack(pady=8, ipadx=25, ipady=7)
        Button(menu, text="Consultar Histórico", bg="#6c757d", fg="white", font=("Arial", 13, "bold"), command=tela_historico).pack(pady=8, ipadx=25, ipady=7)
        Button(menu, text="Avaliar Usuário", bg="#9c27b0", fg="white", font=("Arial", 13, "bold"), command=tela_avaliar).pack(pady=8, ipadx=25, ipady=7)
        Button(menu, text="Sair", bg="#dc3545", fg="white", font=("Arial", 13, "bold"), command=menu_global.destroy).pack(pady=15, ipadx=40, ipady=7)



if __name__ == "__main__":
    iniciar_interface()