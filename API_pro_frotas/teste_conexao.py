import requests


url = "http://api-portal.profrotas.com.br/api/frotista/autorizacao"

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c3VhcmlvLmZyb3RhIjoyNjgsInRva2VuLnRpcG8iOiJBUElfRlJPVElTVEEiLCJ0b2tlbi52ZXJzYW8iOiJQLTAwMDIiLCJpc3MiOiJCb2xlaWEiLCJ0b2tlbi5kYXRhR2VyYWNhbyI6MTcwODcxMTc3MywidXN1YXJpby5wZXJtaXNzb2VzIjpbIkFQSV9GUk9USVNUQSJdLCJleHAiOjE3MTEzMDM3NzMsInVzdWFyaW8uaWQiOi02OTA3NjMyNTAyMTIzMzE0MTYyLCJ1c3VhcmlvLm5vbWUiOiJDYXJnbyBQb2xvIENvbWVyY2lvIExvZ2lzdGljYSBFIFRyYW5zcG9ydGUiLCJ1c3VhcmlvLnRpcG8iOiJGUk9UQSIsInRva2VuLmNvbnRhZG9yUmVub3ZhY29lcyI6MH0.J-50rXUdtEkeV6SgKtbCm8OuFRTTyrLRKecQKAkaN0M'

headers = {
    'Authorization': f'Bearer {token}',
}

response = requests.get(url, headers=headers)

# Verifique o status da resposta
if response.status_code == 200:
    # Se for bem-sucedida, você pode acessar os dados da resposta usando response.json()
    data = response.json()
    print("Sucesso na solicitação. Código de status: ", response.status_code)
else:
    print("Falha na solicitação. Código de status:", response.status_code)