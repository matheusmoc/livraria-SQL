from db_config import connect_to_db

def adicionar_livro(isbn, titulo, autor, editora, genero, preco, qtde_estoque, data_publicacao):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        query = """
        INSERT INTO Livro (ISBN ,Titulo, Autor, Editora, Genero, Preco, Qtde_Estoque, Data_Publicacao)
        VALUES (%s ,%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (isbn, titulo, autor, editora, genero, preco, qtde_estoque, data_publicacao))
        connection.commit()
        print("Livro adicionado com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar livro: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
        else:
            print("Conexão ao banco de dados não foi estabelecida.")

def visualizar_livros():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        query = "SELECT * FROM Livro"
        cursor.execute(query)
        livros = cursor.fetchall()
        for livro in livros:
            print(livro)
    except Exception as e:
        print(f"Erro ao visualizar livros: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def atualizar_livro(id_livro, novo_titulo, novo_autor, nova_editora, novo_genero, novo_preco, nova_qtde_estoque, nova_data_publicacao):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        query = """
        UPDATE Livro
        SET Titulo = %s, Autor = %s, Editora = %s, Genero = %s, Preco = %s, Qtde_Estoque = %s, Data_Publicacao = %s
        WHERE ID_Livro = %s
        """
        cursor.execute(query, (novo_titulo, novo_autor, nova_editora, novo_genero, novo_preco, nova_qtde_estoque, nova_data_publicacao, id_livro))
        connection.commit()
        print("Livro atualizado com sucesso!")
    except Exception as e:
        print(f"Erro ao atualizar livro: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def deletar_livro(id_livro):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        query = "DELETE FROM Livro WHERE ID_Livro = %s"
        cursor.execute(query, (id_livro,))
        connection.commit()
        print("Livro deletado com sucesso!")
    except Exception as e:
        print(f"Erro ao deletar livro: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
