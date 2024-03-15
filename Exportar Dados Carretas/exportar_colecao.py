import json
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import pandas as pd


#Obtendo mês atual
mes_atual = datetime.datetime.now().strftime("%m")
mes_atual = '03'

# Inicialização do Firebase para o primeiro banco de dados
cred1 = credentials.Certificate("Cacapava.json")
app1 = firebase_admin.initialize_app(cred1, name='app1')
db1 = firestore.client(app=app1)

# Inicialização do Firebase para o segundo banco de dados
cred2 = credentials.Certificate("RibeiraoPreto.json")
app2 = firebase_admin.initialize_app(cred2, name='app2')
db2 = firestore.client(app=app2)

# Inicialização do Firebase para o segundo banco de dados
cred3 = credentials.Certificate("Santos.json")
app3 = firebase_admin.initialize_app(cred3, name='app3')
db3= firestore.client(app=app3)

# Inicialização do Firebase para o segundo banco de dados
cred4 = credentials.Certificate("Uberlandia.json")
app4 = firebase_admin.initialize_app(cred4, name='app4')
db4 = firestore.client(app=app4)

def exportar_colecoes():

    # Referência para a coleção no primeiro banco de dados
    colecao_carretas_ref1 = db1.collection('Carretas')

    # Referência para a coleção no segundo banco de dados
    colecao_carretas_ref2 = db2.collection('Carretas')

    # Referência para a coleção no primeiro banco de dados
    colecao_carretas_ref3 = db3.collection('Carretas')

    # Referência para a coleção no segundo banco de dados
    colecao_carretas_ref4 = db4.collection('Carretas')


    # Obter todos os documentos da coleção "Carretas" no primeiro banco de dados
    documentos_carretas1 = colecao_carretas_ref1.where('mes', '==', mes_atual).get()

    # Obter todos os documentos da coleção "Carretas" no segundo banco de dados
    documentos_carretas2 = colecao_carretas_ref2.where('mes', '==', mes_atual).get()

    # Obter todos os documentos da coleção "Carretas" no segundo banco de dados
    documentos_carretas3 = colecao_carretas_ref3.where('mes', '==', mes_atual).get()

    # Obter todos os documentos da coleção "Carretas" no segundo banco de dados
    documentos_carretas4 = colecao_carretas_ref4.where('mes', '==', mes_atual).get()


    # Referência para a coleção "InfoCarretas" no primeiro banco de dados
    colecao_info_carretas_ref1 = db1.collection('InfoCarretas')

    # Referência para a coleção "InfoCarretas" no segundo banco de dados
    colecao_info_carretas_ref2 = db2.collection('InfoCarretas')

    # Referência para a coleção "InfoCarretas" no primeiro banco de dados
    colecao_info_carretas_ref3 = db3.collection('InfoCarretas')

    # Referência para a coleção "InfoCarretas" no segundo banco de dados
    colecao_info_carretas_ref4 = db4.collection('InfoCarretas')

    # Obter todos os documentos da coleção "InfoCarretas" no primeiro banco de dados
    documentos_info_carretas1 = colecao_info_carretas_ref1.where('mes', '==', mes_atual).where('operacao', '==', 'descarga').get()

    # Obter todos os documentos da coleção "InfoCarretas" no segundo banco de dados
    documentos_info_carretas2 = colecao_info_carretas_ref2.where('mes', '==', mes_atual).where('operacao', '==', 'descarga').get()

    # Obter todos os documentos da coleção "InfoCarretas" no primeiro banco de dados
    documentos_info_carretas3 = colecao_info_carretas_ref3.where('mes', '==', mes_atual).where('operacao', '==', 'descarga').get()

    # Obter todos os documentos da coleção "InfoCarretas" no segundo banco de dados
    documentos_info_carretas4 = colecao_info_carretas_ref4.where('mes', '==', mes_atual).where('operacao', '==', 'descarga').get()



    # Obter todos os documentos Saida das Carretas
    documentos_saida_carreta1 = colecao_info_carretas_ref1.where('mes', '==', mes_atual).where('operacao', '==', 'saida').get()

    documentos_saida_carreta2 = colecao_info_carretas_ref2.where('mes', '==', mes_atual).where('operacao', '==', 'saida').get()

    documentos_saida_carreta3 = colecao_info_carretas_ref3.where('mes', '==', mes_atual).where('operacao', '==', 'saida').get()

    documentos_saida_carreta4 = colecao_info_carretas_ref4.where('mes', '==', mes_atual).where('operacao', '==', 'saida').get()



    # Lista para armazenar os documentos serializados de ambos os bancos de dados
    documentos_serializados_carretas = []

    # Iterar sobre todos os documentos da coleção "Carretas" do primeiro banco de dados e serializar
    for documento in documentos_carretas1:
        # Serializar o documento como um dicionário Python
        doc_dict = documento.to_dict()

        # Adicionar o ID do documento ao dicionário
        doc_dict['id'] = documento.id

        # Adicionar o dicionário serializado à lista
        documentos_serializados_carretas.append(doc_dict)

    # Iterar sobre todos os documentos da coleção "Carretas" do segundo banco de dados e serializar
    for documento in documentos_carretas2:
        # Serializar o documento como um dicionário Python
        doc_dict = documento.to_dict()

        # Adicionar o ID do documento ao dicionário
        doc_dict['id'] = documento.id

        # Adicionar o dicionário serializado à lista
        documentos_serializados_carretas.append(doc_dict)

    # Iterar sobre todos os documentos da coleção "Carretas" do segundo banco de dados e serializar
    for documento in documentos_carretas3:
        # Serializar o documento como um dicionário Python
        doc_dict = documento.to_dict()

        # Adicionar o ID do documento ao dicionário
        doc_dict['id'] = documento.id

        # Adicionar o dicionário serializado à lista
        documentos_serializados_carretas.append(doc_dict)

    # Iterar sobre todos os documentos da coleção "Carretas" do segundo banco de dados e serializar
    for documento in documentos_carretas4:
        # Serializar o documento como um dicionário Python
        doc_dict = documento.to_dict()

        # Adicionar o ID do documento ao dicionário
        doc_dict['id'] = documento.id

        # Adicionar o dicionário serializado à lista
        documentos_serializados_carretas.append(doc_dict)


    # Lista para armazenar os documentos serializados da coleção "InfoCarretas"
    documentos_serializados_info_carretas = []


    # Iterar sobre todos os documentos da coleção "InfoCarretas" do primeiro banco de dados e serializar
    for documento in documentos_info_carretas1:
        # Serializar o documento como um dicionário Python
        doc_dict = documento.to_dict()

        # Adicionar o ID do documento ao dicionário
        doc_dict['id'] = documento.id

        # Adicionar o dicionário serializado à lista
        documentos_serializados_info_carretas.append(doc_dict)

    # Iterar sobre todos os documentos da coleção "InfoCarretas" do segundo banco de dados e serializar
    for documento in documentos_info_carretas2:
        # Serializar o documento como um dicionário Python
        doc_dict = documento.to_dict()

        # Adicionar o ID do documento ao dicionário
        doc_dict['id'] = documento.id

        # Adicionar o dicionário serializado à lista
        documentos_serializados_info_carretas.append(doc_dict)

    # Iterar sobre todos os documentos da coleção "InfoCarretas" do segundo banco de dados e serializar
    for documento in documentos_info_carretas3:
        # Serializar o documento como um dicionário Python
        doc_dict = documento.to_dict()

        # Adicionar o ID do documento ao dicionário
        doc_dict['id'] = documento.id

        # Adicionar o dicionário serializado à lista
        documentos_serializados_info_carretas.append(doc_dict)

    # Iterar sobre todos os documentos da coleção "InfoCarretas" do segundo banco de dados e serializar
    for documento in documentos_info_carretas4:
        # Serializar o documento como um dicionário Python
        doc_dict = documento.to_dict()

        # Adicionar o ID do documento ao dicionário
        doc_dict['id'] = documento.id

        # Adicionar o dicionário serializado à lista
        documentos_serializados_info_carretas.append(doc_dict)



    # Iterar sobre todos os documentos SaidaCarreta
    documentos_saida_carretas = []

    for documento in documentos_saida_carreta1:
        # Serializar o documento como um dicionário Python
        doc_dict = documento.to_dict()

        # Adicionar o ID do documento ao dicionário
        doc_dict['id'] = documento.id

        # Adicionar o dicionário serializado à lista
        documentos_saida_carretas.append(doc_dict)

    for documento in documentos_saida_carreta2:
        # Serializar o documento como um dicionário Python
        doc_dict = documento.to_dict()

        # Adicionar o ID do documento ao dicionário
        doc_dict['id'] = documento.id

        # Adicionar o dicionário serializado à lista
        documentos_saida_carretas.append(doc_dict)
    
    for documento in documentos_saida_carreta3:
        # Serializar o documento como um dicionário Python
        doc_dict = documento.to_dict()

        # Adicionar o ID do documento ao dicionário
        doc_dict['id'] = documento.id

        # Adicionar o dicionário serializado à lista
        documentos_saida_carretas.append(doc_dict)

    for documento in documentos_saida_carreta4:
        # Serializar o documento como um dicionário Python
        doc_dict = documento.to_dict()

        # Adicionar o ID do documento ao dicionário
        doc_dict['id'] = documento.id

        # Adicionar o dicionário serializado à lista
        documentos_saida_carretas.append(doc_dict)


    # Escrever todos os documentos serializados em um arquivo JSON
    with open('entrada.json', 'w') as json_file:
        json.dump(documentos_serializados_carretas, json_file, indent=4)

    # Escrever todos os documentos serializados em um arquivo JSON
    with open('descarga.json', 'w') as json_file:
        json.dump(documentos_serializados_info_carretas, json_file, indent=4)

    # Escrever todos os documentos serializados em um arquivo JSON
    with open('saida.json', 'w') as json_file:
        json.dump(documentos_saida_carretas, json_file, indent=4)

    print("Base de dados do banco de dados atualizados com sucesso!!")
    print("\nData e horario atual:")
    print(datetime.datetime.now())
    print("\n\n")

    # df_descarga1 = pd.read_excel( 'Descarga Carreta.xlsx')
    # df_saida1 = pd.read_excel('Saida Carreta.xlsx')
    # df_carretas1 = pd.read_excel('Entrada Carreta.xlsx')


    # Criar um DataFrame a partir dos dados serializados
    df_carretas = pd.DataFrame(documentos_serializados_carretas)
    df_saida = pd.DataFrame(documentos_saida_carretas)
    df_descarga = pd.DataFrame(documentos_serializados_info_carretas)

    # Concatenar os DataFrames
    df_combined = pd.concat([df_carretas, df_descarga, df_saida], ignore_index=True)

    # df_descarga = pd.concat([df_descarga, df_descarga1], ignore_index=True)
    # df_saida = pd.concat([df_saida, df_saida1], ignore_index=True)
    # df_carretas = pd.concat([df_carretas, df_carretas1], ignore_index=True)

    # Agrupar os dados pelo valor na coluna 'dt'
    agg_functions = { 'usuario': 'first', 'filial': 'first','mes':'first', 'palets':'first', 'cheia':'first', 'operacao':'first', 'id':'first', 'cpf':'first', 'horario': 'first', 'placa_carreta': 'first', 'motorista': 'first', 'transportadora': 'first', 'tipo': 'first', 'produto': 'first', 'data_descarga': 'first', 'data_saida':'first','horario':'first', 'horario_descarga':'first', 'horario_saida':'first','veiculo':'first','telefone':'first'}
    

    df_grouped = df_combined.groupby('dt').agg(agg_functions).reset_index()

    # Escrever o DataFrame combinado em um arquivo Excel
    df_combined.to_excel('carretas.xlsx', index=False)
    df_descarga.to_excel('Descarga Carreta.xlsx', index=False)
    df_saida.to_excel('Saida Carreta.xlsx', index=False)
    df_carretas.to_excel('Entrada Carreta.xlsx', index=False)


    # Escrever o DataFrame agrupado em um arquivo Excel
    df_grouped.to_excel('carretas_agrupadas_por_dt.xlsx', index=False)


    print("Arquivo Excel combinado gerado com sucesso!")


exportar_colecoes()

# Agendar a função para ser executada a cada hora
scheduler = BlockingScheduler()
scheduler.add_job(exportar_colecoes, 'interval', hours=1)

# Iniciar o agendador
scheduler.start()