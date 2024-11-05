from Api.config import CLIENT_ID, CLIENT_SECRET, AUTHORIZATION
from Database.config import SERVER, DATABASE, USERNAME, PASSWORD
from Api import notices
from Database import db
from Functions import processing

# Retorna o token de acesso para a conexão com a API
access_token = notices.getAcessToken()

# Pega a resposta da API
notices_data = notices.getNotices(access_token=access_token)

# Verifica se há dados antes de processar
if notices_data:
    # Insere os dados processados no banco de dados
    db.insert_into_database(notices_data)
    print("Dados processados e inseridos com sucesso!.")
else:
    print("Erro ao obter dados da API.")
    