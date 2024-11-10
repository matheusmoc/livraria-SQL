import mysql.connector
from mysql.connector import Error

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost", 
            database="livraria", 
            user="root", 
            password="root"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None


def create_livro_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS livro (
                ISBN VARCHAR(20) PRIMARY KEY,
                Titulo VARCHAR(50) NOT NULL,
                Autor VARCHAR(60) NOT NULL,
                Editora VARCHAR(20) NOT NULL,
                Genero VARCHAR(15) NOT NULL,
                Preco DECIMAL(5,2) NOT NULL,
                Qtde_Estoque INT(3) NOT NULL,
                Data_Publicacao DATE NOT NULL
            )
        '''
        cursor.execute(create_table_query)
        print("Tabela 'livro' verificada/criada com sucesso.")
    except Error as e:
        print(f"Erro ao criar a tabela 'livro': {e}")
    finally:
        cursor.close()

def create_cliente_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS Cliente (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                Nome VARCHAR(50) NOT NULL,
                Email VARCHAR(100) NOT NULL,
                Telefone VARCHAR(15) NOT NULL,
                Endereco TEXT NOT NULL,
                Data_Registro DATE NOT NULL
            )
        '''
        cursor.execute(create_table_query)
        print("Tabela 'Cliente' verificada/criada com sucesso.")
    except Error as e:
        print(f"Erro ao criar a tabela 'Cliente': {e}")
    finally:
        cursor.close()


def create_venda_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS Venda (
                ID_Venda INT AUTO_INCREMENT PRIMARY KEY,
                Data_Venda DATETIME NOT NULL,
                ID_Cliente INT NOT NULL,
                Valor_Total DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (ID_Cliente) REFERENCES Cliente(Id)
            )
        '''
        cursor.execute(create_table_query)
        print("Tabela 'Venda' verificada/criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar a tabela 'Venda': {e}")
    finally:
        cursor.close()
    

def create_item_venda_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS Item_Venda (
                ID_Item_Venda INT AUTO_INCREMENT PRIMARY KEY,
                ID_Venda INT NOT NULL,
                ISBN_Livro VARCHAR(20) NOT NULL,
                Qtde INT NOT NULL,
                Preco_Unitario DECIMAL(5,2) NOT NULL,
                FOREIGN KEY (ID_Venda) REFERENCES Venda(ID_Venda),
                FOREIGN KEY (ISBN_Livro) REFERENCES livro(ISBN)
            )
        '''
        cursor.execute(create_table_query)
        print("Tabela 'Item_Venda' verificada/criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar a tabela 'Item_Venda': {e}")
    finally:
        cursor.close()