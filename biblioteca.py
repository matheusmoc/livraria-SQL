from models.livros import adicionar_livro, visualizar_livros, atualizar_livro, deletar_livro
from models.clientes import adicionar_cliente, visualizar_clientes
from models.venda import registrar_venda, historico_vendas
from db_config import create_cliente_table, create_livro_table, create_venda_table, create_item_venda_table, connect_to_db
import random

def menu():
    connection = connect_to_db()
    if connection:
        create_livro_table(connection)
        create_cliente_table(connection)
        create_venda_table(connection)
        create_item_venda_table(connection)

    while True:
        print("\nSistema de Biblioteca")
        print("1. Adicionar Livro")
        print("2. Visualizar Livros")
        print("3. Atualizar Livro")
        print("4. Deletar Livro")
        print("5. Adicionar Cliente")
        print("6. Visualizar Clientes")
        print("7. Registrar Venda")
        print("8. Ver Histórico de Vendas")
        print("9. Sair")
        escolha = input("Escolha uma opção: ")

        match escolha:
            case "1":
                isbn = random.randint(1000000000000, 9999999999999)
                titulo = input("Digite o título do livro: ")
                autor = input("Digite o autor do livro: ")
                editora = input("Digite a editora do livro: ")
                genero = input("Digite o gênero do livro: ")
                preco = float(input("Digite o preço do livro: "))
                qtde_estoque = int(input("Digite a quantidade em estoque: "))
                data_publicacao = input("Digite a data de publicação (YYYY-MM-DD): ")
                adicionar_livro(isbn, titulo, autor, editora, genero, preco, qtde_estoque, data_publicacao)
            case "2":
                visualizar_livros()
            case "3":
                id_livro = int(input("Digite o ISNB do livro a ser deletado: "))
                novo_titulo = input("Novo título: ")
                novo_autor = input("Novo autor: ")
                nova_editora = input("Nova editora: ")
                novo_genero = input("Novo gênero: ")
                novo_preco = float(input("Novo preço: "))
                nova_qtde_estoque = int(input("Nova quantidade: "))
                nova_data_publicacao = input("Nova data de publicação (YYYY-MM-DD): ")
                atualizar_livro(id_livro, novo_titulo, novo_autor, nova_editora, novo_genero, novo_preco, nova_qtde_estoque, nova_data_publicacao)
            case "4":
                id_livro = int(input("Digite o ISNB do livro a ser deletado: "))
                deletar_livro(id_livro)
            case "5":
                nome = input("Nome do cliente: ")
                email = input("E-mail do cliente: ")
                telefone = input("Telefone do cliente: ")
                endereco = input("Endereço do cliente: ")
                adicionar_cliente(nome, email, telefone, endereco)
            case "6":
                visualizar_clientes()
            case "7":
                id_cliente = int(input("Digite o ID do cliente: "))
                livros_vendidos = []
                while True:
                    isbn = input("Digite o ISBN do livro a ser comprado (0 para finalizar): ")
                    if isbn == "0":
                        break
                    qtde = int(input("Digite a quantidade: "))
                    livros_vendidos.append({'ISBN': isbn, 'Qtde': qtde})

                registrar_venda(connection, id_cliente, livros_vendidos)
            case "8":
                historico_vendas(connection) 
            case "9":
                print("Saindo do sistema.")
                break
            case _:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
