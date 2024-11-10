from db_config import connect_to_db

def adicionar_cliente(nome, email, telefone, endereco, data_registro):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        query = """
        INSERT INTO Cliente (Nome, Email, Telefone, Endereco, Data_Registro)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nome, email, telefone, endereco, data_registro))
        connection.commit()
        print("Cliente adicionado com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar cliente: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def visualizar_clientes():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        query = "SELECT * FROM Cliente"
        cursor.execute(query)
        clientes = cursor.fetchall()
        for cliente in clientes:
            print(cliente)
    except Exception as e:
        print(f"Erro ao visualizar clientes: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
