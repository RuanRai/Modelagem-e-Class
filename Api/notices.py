import requests
from config import CLIENT_ID, CLIENT_SECRET, AUTHORIZATION

class NextiAPI:
    
    @classmethod
    def get_access_token(cls):
        """
        Obtém um token de acesso usando credenciais de cliente.
        """
        token_url = "https://api.nexti.com/security/oauth/token"

        # Parâmetros da solicitação
        params = {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }

        # Cabeçalhos da solicitação
        headers = {
            "Content-Type": "application/json",
            "Authorization": AUTHORIZATION
        }

        try:
            # Realizar a solicitação para obter o token de acesso
            response = requests.post(token_url, params=params, headers=headers)
            response.raise_for_status()  # Lança um erro se a solicitação não for bem-sucedida

            # Extrai o token de acesso da resposta
            token_data = response.json()
            access_token = token_data.get('access_token')
            print("Token de acesso obtido com sucesso.")

            return access_token
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter o token de acesso: {e}")
            return None

    @classmethod
    def get_notices(cls, access_token, filter='Colaborador', page=0, size='9999999'):
        """
        Obtém notificações da API e processa os dados.
        """
        request_url = "https://api.nexti.com/notices/all"

        # Parâmetros da solicitação
        payload = {
            "filter": filter,
            "page": page,
            "size": size,
        }

        # Cabeçalhos da solicitação
        headers = {
            "Authorization": f"Bearer {access_token}",
            "accept": "*/*",
        }

        try:
            # Realize a requisição GET
            response = requests.get(request_url, params=payload, headers=headers)
            response.raise_for_status()  # Lança um erro se a solicitação não for bem-sucedida

            # Extrai apenas o conteúdo relevante da resposta
            content_data = response.json().get('content', [])

            # Lista para armazenar os dados segregados
            segregated_data = []

            # Itera sobre os itens em content_data
            for item in content_data:
                persons = item.get('persons', [])
                persons_external_ids = item.get('personsExternalIds', [])

                # Garante que as listas tenham o mesmo comprimento
                min_len = min(len(persons), len(persons_external_ids))

                # Cria uma nova entrada para cada pessoa
                for i in range(min_len):
                    new_entry = item.copy()
                    new_entry['persons'] = persons[i]
                    new_entry['personsExternalIds'] = persons_external_ids[i]
                    segregated_data.append(new_entry)

            print("Dados obtidos com sucesso!")

            return segregated_data
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter dados da API: {e}")
            return None
