import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# Inicialização do Firebase para o primeiro banco de dados
cred1 = credentials.Certificate("serviceAccount1.json")
app1 = firebase_admin.initialize_app(cred1, name='app1')
db1 = firestore.client(app=app1)

# Ler a planilha Excel usando pandas
excel_file_path = "escala.xlsx"
df = pd.read_excel(excel_file_path)

# Converter o DataFrame do pandas para um dicionário
data_dict = df.to_dict(orient="records")

# Enviar os dados para o primeiro banco de dados
collection_ref1 = db1.collection("Escala")
for data in data_dict:
    # Adicionar cada registro como um documento na coleção
    collection_ref1.add(data)

# Finalizar as aplicações do Firebase (opcional)
firebase_admin.delete_app(firebase_admin.get_app(name='app1'))
