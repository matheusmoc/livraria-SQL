from db_config import connect_to_db

def registrar_venda(connection, id_cliente, livros_vendidos):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        data_venda = "NOW()" 
        valor_total = sum([livro['Qtde'] * livro['Preco_Unitario'] for livro in livros_vendidos])

        query_venda = """
        INSERT INTO Venda (Data_Venda, ID_Cliente, Valor_Total)
        VALUES (NOW(), %s, %s)
        """
        cursor.execute(query_venda, (id_cliente, valor_total))
        connection.commit()

        id_venda = cursor.lastrowid

        for livro in livros_vendidos:
            query_item_venda = """
            INSERT INTO Item_Venda (ID_Venda, ID_Livro, Qtde, Preco_Unitario)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_item_venda, (id_venda, livro['ID_Livro'], livro['Qtde'], livro['Preco_Unitario']))
            connection.commit()

        print("Venda registrada com sucesso!")
        
    except Exception as e:
        print(f"Erro ao registrar venda: {e}")
    finally:
        if connection.is_connected():
            cursor.close()

