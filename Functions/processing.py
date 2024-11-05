from Api.notices import response

token_data = response.json()
access_token = token_data.get('access_token')
print("Token de acesso obtido com sucesso.")

content_data = response.json().get('content', [])
