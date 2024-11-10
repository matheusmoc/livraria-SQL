from db_config import connect_to_db


def registrar_venda(connection, id_cliente, livros_vendidos):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        valor_total = 0

        for livro in livros_vendidos:
            isbn = livro['ISBN']
            qtde = livro['Qtde']
            
            print(f"Consultando ISBN: {isbn}") 
            
            # Consulta para obter o preço do livro diretamente pelo ISBN
            query_preco = "SELECT Preco FROM Livro WHERE ISBN = %s"
            cursor.execute(query_preco, (isbn,))
            result = cursor.fetchone()
            
            if result:
                preco_unitario = result[0]
                valor_total += qtde * preco_unitario
            else:
                print(f"Erro: ISBN {isbn} não encontrado na base de dados.")
                return  

        query_venda = """
        INSERT INTO Venda (Data_Venda, ID_Cliente, Valor_Total)
        VALUES (NOW(), %s, %s)
        """
        cursor.execute(query_venda, (id_cliente, valor_total))
        connection.commit()

        id_venda = cursor.lastrowid

        for livro in livros_vendidos:
            isbn = livro['ISBN']
            qtde = livro['Qtde']


            query_buscar_preco = "SELECT Preco FROM Livro WHERE ISBN = %s"
            cursor.execute(query_buscar_preco, (isbn,))
            result = cursor.fetchone()

            if result:
                preco_unitario = result[0]

                query_item_venda = """
                INSERT INTO Item_Venda (ID_Venda, ISBN_Livro, Qtde, Preco_Unitario)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query_item_venda, (id_venda, isbn, qtde, preco_unitario))
                connection.commit()
            else:
                print(f"Erro: ISBN {isbn} não encontrado na base de dados.")

        print("Venda registrada com sucesso!")

    except Exception as e:
        print(f"Erro ao registrar venda: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def historico_vendas(connection):
    try:
        cursor = connection.cursor()
        
        # As letras aleatorias são ALIAS
        # No caso, ao invés de escrever Venda.ID_Venda, Venda.Data_Venda, Venda.Valor_Total, e Cliente.Nome, 
        # você usa v.ID_Venda, v.Data_Venda, v.Valor_Total, e c.Nome respectivamente. 

        query = """
        SELECT v.ID_Venda, v.Data_Venda, v.Valor_Total, c.Nome 
        FROM Venda v
        JOIN Cliente c ON v.ID_Cliente = c.Id
        ORDER BY v.Data_Venda DESC
        """
        cursor.execute(query)
        vendas = cursor.fetchall()
        
        if not vendas:
            print("Nenhuma venda registrada.")
            return

        for venda in vendas:
            id_venda, data_venda, valor_total, nome_cliente = venda
            print(f"\nVenda ID: {id_venda}")
            print(f"Data da Venda: {data_venda}")
            print(f"Cliente: {nome_cliente}")
            print(f"Valor Total: R${valor_total:.2f}")
        
    except Exception as e:
        print(f"Erro ao consultar o histórico de vendas: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()