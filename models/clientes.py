from db_config import connect_to_db
from datetime import datetime

def adicionar_cliente(nome, email, telefone, endereco):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        data_registro = datetime.now() 
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
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Cliente"
        cursor.execute(query)
        clientes = cursor.fetchall()  
        
        print(clientes)

        if not clientes:
            print("Nenhum cliente encontrado.")
            return None
        return clientes  

    except Exception as e:
        print(f"Erro ao visualizar clientes: {e}")
        return None 

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()