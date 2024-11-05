import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from config import SERVER, DATABASE, USERNAME, PASSWORD

class DatabaseInserter:
    
    @classmethod
    def convert_date_string(cls, date_str):
        """
        Converte uma string de data no formato "ddMMyyyyHHmmss" para um objeto datetime.
        """
        return datetime.strptime(date_str, "%d%m%Y%H%M%S")
    
    @classmethod
    def insert_into_database(cls, data):
        """
        Insere dados em uma tabela do SQL Server.
        """
        # Configurações do banco de dados
        server = SERVER
        database = DATABASE
        username = USERNAME
        password = PASSWORD

        # Cria a string de conexão para o SQLAlchemy
        connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
        
        # Cria a conexão com o banco de dados
        engine = create_engine(connection_string)

        # Converte a lista para um DataFrame
        df = pd.DataFrame(data)

        # Converte as strings de data para objetos datetime
        df['startDate'] = df['startDate'].apply(cls.convert_date_string)
        df['finishDate'] = df['finishDate'].apply(cls.convert_date_string)

        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Iniciando a inserção de dados na tabela em {current_time}...")
            
            # Obtém o número de registros antes da inserção
            num_rows_before = pd.read_sql_query('SELECT COUNT(*) FROM NEXTI_ConvocacoesAvisos', engine).iloc[0, 0]
            print(f"Número de registros na tabela antes da inserção: {num_rows_before}")

            # Insere os dados na tabela do SQL Server
            df.to_sql('NEXTI_ConvocacoesAvisos', con=engine, if_exists='replace', index=False)

            # Obtém o número de registros após a inserção
            num_rows_after = pd.read_sql_query('SELECT COUNT(*) FROM NEXTI_ConvocacoesAvisos', engine).iloc[0, 0]
            print(f"Número de registros na tabela após a inserção: {num_rows_after}")
            print("Dados inseridos com sucesso na tabela.")
        except SQLAlchemyError as e:
            print(f"Erro ao inserir dados na tabela: {e}")
            for error in e.orig.args:
                if isinstance(error, tuple) and len(error) > 1:
                    column_name = error[1]
                    print(f"Problema na coluna: {column_name}")
        finally:
            # Fecha a conexão com o banco de dados
            engine.dispose()
