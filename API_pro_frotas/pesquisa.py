import requests
import json
import firebase_admin
from firebase_admin import credentials, firestore

#Carregando as credenciais do Firebase
cred = credentials.Certificate("credencial.json")
firebase_admin.initialize_app(cred)


url = "http://api-portal.profrotas.com.br/api/frotista/postoCredenciado/pesquisa"

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c3VhcmlvLmZyb3RhIjoyNjgsInRva2VuLnRpcG8iOiJBUElfRlJPVElTVEEiLCJ0b2tlbi52ZXJzYW8iOiJQLTAwMDIiLCJpc3MiOiJCb2xlaWEiLCJ0b2tlbi5kYXRhR2VyYWNhbyI6MTcwODcxMTc3MywidXN1YXJpby5wZXJtaXNzb2VzIjpbIkFQSV9GUk9USVNUQSJdLCJleHAiOjE3MTEzMDM3NzMsInVzdWFyaW8uaWQiOi02OTA3NjMyNTAyMTIzMzE0MTYyLCJ1c3VhcmlvLm5vbWUiOiJDYXJnbyBQb2xvIENvbWVyY2lvIExvZ2lzdGljYSBFIFRyYW5zcG9ydGUiLCJ1c3VhcmlvLnRpcG8iOiJGUk9UQSIsInRva2VuLmNvbnRhZG9yUmVub3ZhY29lcyI6MH0.J-50rXUdtEkeV6SgKtbCm8OuFRTTyrLRKecQKAkaN0M'

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

payload = {
"pagina": 1,
"ordenacao": None
}

response = requests.post(url, headers=headers, json=payload)

# Verifique o status da resposta
if response.status_code == 200:
    # Se for bem-sucedida, você pode acessar os dados da resposta usando response.json()
    data = response.json()
    print(data)

    with open('pro_frotas.json', 'w') as arquivo:
        json.dump(data, arquivo)

    # Inicializar o firestore
    db = firestore.client()

    for registro in data['registros']:  # Iterar sobre os registros em data['registros']
        documento = registro  # Não é necessário fazer qualquer conversão
        db.collection('postos').add(documento)

    print("Dados adicionados ao Firestore com sucesso!")

else:
    print("Falha na solicitação. Código de status:", response.status_code)