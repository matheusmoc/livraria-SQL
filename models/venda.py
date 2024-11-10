from db_config import connect_to_db



connection = connect_to_db()

def fetch_book_price(cursor, isbn):

    query = "SELECT Preco FROM Livro WHERE ISBN = %s"
    cursor.execute(query, (isbn,))
    result = cursor.fetchone()
    if result:
        return result[0]
    print(f"Erro: ISBN {isbn} não encontrado na base de dados.")
    return None


def calculate_total_value(cursor, livros_vendidos):

    valor_total = 0
    for livro in livros_vendidos:
        isbn = livro['ISBN']
        qtde = livro['Qtde']
        
        print(f"Consultando ISBN: {isbn}") 
        preco_unitario = fetch_book_price(cursor, isbn)
        if preco_unitario is not None:
            valor_total += qtde * preco_unitario
        else:
            print(f"Erro: ISBN {isbn} não encontrado.")
            return None
    return valor_total


def insert_sale(cursor, id_cliente, valor_total):

    query = """
    INSERT INTO Venda (Data_Venda, ID_Cliente, Valor_Total)
    VALUES (NOW(), %s, %s)
    """
    cursor.execute(query, (id_cliente, valor_total))
    return cursor.lastrowid

def update_stock(cursor, isbn, qtde):
    query_check_stock = "SELECT Qtde_Estoque FROM Livro WHERE ISBN = %s"
    cursor.execute(query_check_stock, (isbn,))
    result = cursor.fetchone()

    if result:
        current_stock = result[0]
        print(f"Current stock for ISBN {isbn}: {current_stock}")
        if current_stock >= qtde:
            query_update_stock = "UPDATE Livro SET Qtde_Estoque = Qtde_Estoque - %s + 1 WHERE ISBN = %s"
            cursor.execute(query_update_stock, (qtde, isbn))
            connection.commit()
            print(f"Updated stock for ISBN {isbn}: {current_stock - qtde}")
        else:
            print(f"Erro: Estoque insuficiente para o ISBN {isbn}.")
            return False
    else:
        print(f"Erro: ISBN {isbn} não encontrado na base de dados.")
        return False
    return True

def insert_sale_items(cursor, id_venda, livros_vendidos):

    for livro in livros_vendidos:
        isbn = livro['ISBN']
        qtde = livro['Qtde']
        
        preco_unitario = fetch_book_price(cursor, isbn)
        if preco_unitario is not None:
            if update_stock(cursor, isbn, qtde):  
                query = """
                INSERT INTO Item_Venda (ID_Venda, ISBN_Livro, Qtde, Preco_Unitario)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (id_venda, isbn, qtde, preco_unitario))
            else:
                print(f"Erro: Não foi possível registrar a venda para o ISBN {isbn} devido a estoque insuficiente.")
        else:
            print(f"Erro: ISBN {isbn} não encontrado na base de dados.")


def registrar_venda(connection, id_cliente, livros_vendidos):
    try:
        cursor = connection.cursor()
        valor_total = calculate_total_value(cursor, livros_vendidos)
        
        if valor_total is None:
            return  

        id_venda = insert_sale(cursor, id_cliente, valor_total)
        insert_sale_items(cursor, id_venda, livros_vendidos)
        
        connection.commit()
        print("Venda registrada com sucesso!")

    except Exception as e:
        print(f"Erro ao registrar venda: {e}")
        connection.rollback()
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# def registrar_venda(connection, id_cliente, livros_vendidos):
#     connection = connect_to_db()
#     cursor = connection.cursor()
    
#     create_trigger_stock(cursor)
    
#     try:
#         valor_total = calculate_total_value(cursor, livros_vendidos)
#         if valor_total is None:
#             return  

#         id_venda = insert_sale(cursor, id_cliente, valor_total)
#         insert_sale_items(cursor, id_venda, livros_vendidos)
        
#         connection.commit()
#         print("Venda registrada com sucesso!")

#     except Exception as e:
#         print(f"Erro ao registrar venda: {e}")
#         connection.rollback()
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()



def historico_vendas(connection):
    """
    Retrieves the sales history along with the books purchased in each sale.
    """
    vendas = []
    try:
        cursor = connection.cursor()
        query = """
        SELECT v.ID_Venda, v.Data_Venda, v.Valor_Total, c.Nome, l.Titulo, iv.Qtde
        FROM Venda v
        JOIN Cliente c ON v.ID_Cliente = c.Id
        JOIN Item_Venda iv ON v.ID_Venda = iv.ID_Venda
        JOIN livro l ON iv.ISBN_Livro = l.ISBN
        ORDER BY v.Data_Venda DESC
        """
        cursor.execute(query)
        vendas = cursor.fetchall()

        for venda in vendas:
            id_venda, data_venda, valor_total, nome_cliente, livro_titulo, quantidade = venda
            print(f"\nVenda ID: {id_venda}")
            print(f"Data da Venda: {data_venda}")
            print(f"Cliente: {nome_cliente}")
            print(f"Valor Total: R${valor_total:.2f}")
            print(f"Livro Comprado: {livro_titulo}")
            print(f"Quantidade: {quantidade}")

        return vendas
    
    except Exception as e:
        print(f"Erro ao consultar o histórico de vendas: {e}")
    