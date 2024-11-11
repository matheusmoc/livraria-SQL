import tkinter as tk
from tkinter import messagebox, ttk
from models.livros import adicionar_livro, visualizar_livros, atualizar_livro, deletar_livro
from models.clientes import adicionar_cliente, visualizar_clientes
from models.venda import registrar_venda, historico_vendas
from db_config import create_cliente_table, create_livro_table, create_venda_table, create_item_venda_table, connect_to_db
import random

connection = connect_to_db()

def configure_style():
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 12), padding=10, width=25)
    style.configure('TLabel', font=('Arial', 12))
    style.configure('TEntry', font=('Arial', 12), padding=5)


def adicionar_livro_gui():
    def salvar_livro():
        isbn = random.randint(1000000000000, 9999999999999)
        titulo = entry_titulo.get()
        autor = entry_autor.get()
        editora = entry_editora.get()
        genero = entry_genero.get()
        preco = float(entry_preco.get())
        qtde_estoque = int(entry_qtde_estoque.get())
        data_publicacao = entry_data_publicacao.get()

        adicionar_livro(isbn, titulo, autor, editora, genero, preco, qtde_estoque, data_publicacao)
        messagebox.showinfo("Sucesso", "Livro adicionado com sucesso!")
        adicionar_livro_window.destroy()

    adicionar_livro_window = tk.Toplevel()
    adicionar_livro_window.title("Adicionar Livro")
    adicionar_livro_window.geometry("400x300")

    tk.Label(adicionar_livro_window, text="Título").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_titulo = tk.Entry(adicionar_livro_window)
    entry_titulo.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(adicionar_livro_window, text="Autor").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_autor = tk.Entry(adicionar_livro_window)
    entry_autor.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(adicionar_livro_window, text="Editora").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_editora = tk.Entry(adicionar_livro_window)
    entry_editora.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(adicionar_livro_window, text="Gênero").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_genero = tk.Entry(adicionar_livro_window)
    entry_genero.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(adicionar_livro_window, text="Preço").grid(row=4, column=0, sticky="w", padx=10, pady=5)
    entry_preco = tk.Entry(adicionar_livro_window)
    entry_preco.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(adicionar_livro_window, text="Quantidade em Estoque").grid(row=5, column=0, sticky="w", padx=10, pady=5)
    entry_qtde_estoque = tk.Entry(adicionar_livro_window)
    entry_qtde_estoque.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(adicionar_livro_window, text="Data de Publicação (YYYY-MM-DD)").grid(row=6, column=0, sticky="w", padx=10, pady=5)
    entry_data_publicacao = tk.Entry(adicionar_livro_window)
    entry_data_publicacao.grid(row=6, column=1, padx=10, pady=5)

    ttk.Button(adicionar_livro_window, text="Salvar", command=salvar_livro).grid(row=7, column=0, columnspan=2, pady=15)


def visualizar_livros_gui():
    livros = visualizar_livros() 
    if livros is None:
        print("Nenhum livro encontrado.")
        return
    
    livros_window = tk.Toplevel()
    livros_window.title("Livros")
    livros_window.geometry("600x400")

    canvas = tk.Canvas(livros_window)
    canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar = tk.Scrollbar(livros_window, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")

    canvas.configure(yscrollcommand=scrollbar.set)
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_frame_configure)

    for index, livro in enumerate(livros):
        livro_frame = tk.Frame(frame)
        livro_frame.grid(row=index, column=0, padx=10, pady=10, sticky="w")
        
        tk.Label(livro_frame, text=f"Título: {livro['Titulo']}").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tk.Label(livro_frame, text=f"Autor: {livro['Autor']}").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        tk.Label(livro_frame, text=f"ISBN: {livro['ISBN']}").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        tk.Label(livro_frame, text=f"Preço: R${livro['Preco']}").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        tk.Label(livro_frame, text=f"Quantidade: {livro['Qtde_Estoque']}").grid(row=4, column=0, sticky="w", padx=10, pady=5)

        separator = tk.Label(livro_frame, text="-"*40)
        separator.grid(row=5, column=0, sticky="w", padx=10, pady=5)

def atualizar_livro_gui():
    def salvar_atualizacao():
        isbn = entry_isbn.get()
        novo_titulo = entry_titulo.get()
        novo_autor = entry_autor.get()
        nova_editora = entry_editora.get()
        novo_genero = entry_genero.get()
        novo_preco = float(entry_preco.get())
        nova_qtde_estoque = int(entry_qtde_estoque.get())
        nova_data_publicacao = entry_data_publicacao.get()

        atualizar_livro(isbn, novo_titulo, novo_autor, nova_editora, novo_genero, novo_preco, nova_qtde_estoque, nova_data_publicacao)
        messagebox.showinfo("Sucesso", "Livro atualizado com sucesso!")
        atualizar_livro_window.destroy()

    atualizar_livro_window = tk.Toplevel()
    atualizar_livro_window.title("Atualizar Livro")
    atualizar_livro_window.geometry("400x300")

    tk.Label(atualizar_livro_window, text="ISBN").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_isbn = tk.Entry(atualizar_livro_window)
    entry_isbn.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(atualizar_livro_window, text="Título").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_titulo = tk.Entry(atualizar_livro_window)
    entry_titulo.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(atualizar_livro_window, text="Autor").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_autor = tk.Entry(atualizar_livro_window)
    entry_autor.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(atualizar_livro_window, text="Editora").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_editora = tk.Entry(atualizar_livro_window)
    entry_editora.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(atualizar_livro_window, text="Gênero").grid(row=4, column=0, sticky="w", padx=10, pady=5)
    entry_genero = tk.Entry(atualizar_livro_window)
    entry_genero.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(atualizar_livro_window, text="Preço").grid(row=5, column=0, sticky="w", padx=10, pady=5)
    entry_preco = tk.Entry(atualizar_livro_window)
    entry_preco.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(atualizar_livro_window, text="Quantidade em Estoque").grid(row=6, column=0, sticky="w", padx=10, pady=5)
    entry_qtde_estoque = tk.Entry(atualizar_livro_window)
    entry_qtde_estoque.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(atualizar_livro_window, text="Data de Publicação (YYYY-MM-DD)").grid(row=7, column=0, sticky="w", padx=10, pady=5)
    entry_data_publicacao = tk.Entry(atualizar_livro_window)
    entry_data_publicacao.grid(row=7, column=1, padx=10, pady=5)
    
    ttk.Button(atualizar_livro_window, text="Salvar", command=salvar_atualizacao).grid(row=8, column=0, columnspan=2, pady=15)

def deletar_livro_gui():
    def excluir_livro():
        isbn = entry_isbn.get()

        deletar_livro(isbn)
        messagebox.showinfo("Sucesso", "Livro deletado com sucesso!")
        deletar_livro_window.destroy()

    deletar_livro_window = tk.Toplevel()
    deletar_livro_window.title("Deletar Livro")
    deletar_livro_window.geometry("400x200")

    tk.Label(deletar_livro_window, text="ISBN do Livro").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_isbn = tk.Entry(deletar_livro_window)
    entry_isbn.grid(row=0, column=1, padx=10, pady=5)

    ttk.Button(deletar_livro_window, text="Excluir", command=excluir_livro).grid(row=1, column=0, columnspan=2, pady=15)

def adicionar_cliente_gui():
    def salvar_cliente():
        nome = entry_nome.get()
        email = entry_email.get()
        telefone = entry_telefone.get()
        endereco = entry_endereco.get()

        adicionar_cliente(nome, email, telefone, endereco)
        messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")
        adicionar_cliente_window.destroy()

    adicionar_cliente_window = tk.Toplevel()
    adicionar_cliente_window.title("Adicionar Cliente")
    adicionar_cliente_window.geometry("400x300")

    tk.Label(adicionar_cliente_window, text="Nome").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_nome = tk.Entry(adicionar_cliente_window)
    entry_nome.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(adicionar_cliente_window, text="E-mail").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_email = tk.Entry(adicionar_cliente_window)
    entry_email.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(adicionar_cliente_window, text="Telefone").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_telefone = tk.Entry(adicionar_cliente_window)
    entry_telefone.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(adicionar_cliente_window, text="Endereço").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_endereco = tk.Entry(adicionar_cliente_window)
    entry_endereco.grid(row=3, column=1, padx=10, pady=5)

    ttk.Button(adicionar_cliente_window, text="Salvar", command=salvar_cliente).grid(row=4, column=0, columnspan=2, pady=15)

def visualizar_clientes_gui():
    clientes = visualizar_clientes()
    
    if clientes is None:
        print("Nenhum cliente encontrado.")
        return
    
    clientes_window = tk.Toplevel()
    clientes_window.title("Clientes")
    clientes_window.geometry("400x300")
    
    canvas = tk.Canvas(clientes_window)
    canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar = tk.Scrollbar(clientes_window, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    
    canvas.configure(yscrollcommand=scrollbar.set)
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    for index, cliente in enumerate(clientes):
        cliente_frame = tk.Frame(frame)
        cliente_frame.grid(row=index, column=0, padx=10, pady=10, sticky="w")

        title_label = tk.Label(cliente_frame, text=f"Cliente {index + 1}")
        title_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        tk.Label(cliente_frame, text=f"Nome: {cliente['Nome']}").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        tk.Label(cliente_frame, text=f"Email: {cliente['Email']}").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        tk.Label(cliente_frame, text=f"Telefone: {cliente['Telefone']}").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        tk.Label(cliente_frame, text=f"Endereço: {cliente['Endereco']}").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        tk.Label(cliente_frame, text=f"Data de Registro: {cliente['Data_Registro']}").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        
        separator = tk.Label(cliente_frame, text="-"*40)
        separator.grid(row=6, column=0, sticky="w", padx=10, pady=5)

    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def registrar_venda_gui(connection):
    def salvar_venda():
        selected_customer = combo_clientes.get()
        if not selected_customer:
            messagebox.showerror("Erro", "Selecione um cliente!")
            return
        id_cliente = clientes_dict.get(selected_customer)
        
        if not id_cliente:
            messagebox.showerror("Erro", "Cliente inválido!")
            return
        
        livros_vendidos = []
        while True:
            isbn = entry_isbn.get()
            if isbn == "0":
                break

            qtde_str = entry_qtde.get()
            if not qtde_str.isdigit() or int(qtde_str) <= 0:
                messagebox.showerror("Erro", "Quantidade inválida! Insira um número inteiro positivo.")
                return

            qtde = int(qtde_str)
            livros_vendidos.append({'ISBN': isbn, 'Qtde': qtde})
            break

        if livros_vendidos:
            registrar_venda(connection, id_cliente, livros_vendidos)
            messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
        else:
            messagebox.showwarning("Atenção", "Nenhum livro foi registrado.")


    cursor = connection.cursor()
    cursor.execute("SELECT Id, Nome FROM Cliente")
    clientes = cursor.fetchall()
    
    clientes_dict = {nome: id_cliente for id_cliente, nome in clientes}

    registrar_venda_window = tk.Toplevel()
    registrar_venda_window.title("Registrar Venda")
    registrar_venda_window.geometry("400x300")

    tk.Label(registrar_venda_window, text="Selecione o Cliente").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    combo_clientes = ttk.Combobox(registrar_venda_window, values=list(clientes_dict.keys()), state="readonly")
    combo_clientes.grid(row=0, column=1, padx=10, pady=5)
    combo_clientes.update_idletasks() 

    tk.Label(registrar_venda_window, text="ISBN do Livro").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_isbn = tk.Entry(registrar_venda_window)
    entry_isbn.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(registrar_venda_window, text="Quantidade").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_qtde = tk.Entry(registrar_venda_window)
    entry_qtde.grid(row=2, column=1, padx=10, pady=5)

    ttk.Button(registrar_venda_window, text="Registrar Venda", command=salvar_venda).grid(row=3, column=0, columnspan=2, pady=15)
    tk.Label(registrar_venda_window, text="Digite ISBN do livro e Quantidade. Digite 0 para finalizar.").grid(row=4, column=0, columnspan=2, pady=10)

def historico_vendas_gui(connection):
    vendas = historico_vendas(connection)

    vendas_window = tk.Toplevel()
    vendas_window.title("Histórico de Vendas")
    vendas_window.geometry("400x300")

    canvas = tk.Canvas(vendas_window)
    canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar = tk.Scrollbar(vendas_window, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    
    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    for index, venda in enumerate(vendas):
        id_venda, data_venda, valor_total, nome_cliente, livro_titulo, quantidade = venda
        venda_frame = tk.Frame(frame)
        venda_frame.grid(row=index, column=0, padx=10, pady=10, sticky="w")

        title_label = tk.Label(venda_frame, text=f"Venda {index + 1}")
        title_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        tk.Label(venda_frame, text=f"Venda ID: {id_venda}").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        tk.Label(venda_frame, text=f"Cliente: {nome_cliente}").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        tk.Label(venda_frame, text=f"Data: {data_venda}").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        tk.Label(venda_frame, text=f"Valor Total: R${valor_total:.2f}").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        tk.Label(venda_frame, text=f"Livro Comprado: {livro_titulo}").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        tk.Label(venda_frame, text=f"Quantidade: {quantidade}").grid(row=6, column=0, sticky="w", padx=10, pady=5)

        separator = tk.Label(venda_frame, text="-"*40)
        separator.grid(row=7, column=0, sticky="w", padx=10, pady=5)

    frame.update_idletasks()  
    canvas.config(scrollregion=canvas.bbox("all"))

    vendas_window.grid_rowconfigure(0, weight=1)
    vendas_window.grid_columnconfigure(0, weight=1)

def main_menu():
    root = tk.Tk()
    root.title("Sistema de Livraria")
    root.geometry("400x500")

    configure_style() 

    ttk.Label(root, text="Livraria", font=('Arial', 16)).pack(pady=10)
    ttk.Button(root, text="Adicionar Livro", command=adicionar_livro_gui).pack(pady=10, fill="x")
    ttk.Button(root, text="Visualizar Livros", command=visualizar_livros_gui).pack(pady=10, fill="x")
    ttk.Button(root, text="Atualizar Livros", command=atualizar_livro_gui).pack(pady=10, fill="x")
    ttk.Button(root, text="Deletar Livros", command=deletar_livro_gui).pack(pady=10, fill="x")
    ttk.Button(root, text="Adicionar Cliente", command=adicionar_cliente_gui).pack(pady=10, fill="x")
    ttk.Button(root, text="Visualizar Clientes", command=visualizar_clientes_gui).pack(pady=10, fill="x")
    ttk.Button(root, text="Registrar Venda", command=lambda: registrar_venda_gui(connection)).pack(pady=10, fill="x")
    ttk.Button(root, text="Histórico de Vendas", command=lambda: historico_vendas_gui(connection)).pack(pady=10, fill="x")

    root.mainloop()


if __name__ == "__main__":
    create_cliente_table(connection)
    create_livro_table(connection)
    create_venda_table(connection)
    create_item_venda_table(connection)

    main_menu()
