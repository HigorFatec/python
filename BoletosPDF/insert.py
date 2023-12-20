import pyodbc
import pandas as pd


SERVER = '177.47.20.123,1433'
DATABASE = 'CargoPoloTemp'
USERNAME = 'pydesenv'
PASSWORD = 'c9N5HA3Cv6Lyo6'
connectionString = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
conn = pyodbc.connect(connectionString)

df = pd.read_excel('Boletos.xlsx')
df_filtrado = df[(df['CONFERE'] == 'ERRO') & (df['LANCADO RODOPAR'] == 'OK')]

print(df)

# Solicita ao usuário que insira o índice da linha
indice_linha = int(input("Digite o índice da linha que deseja executar: "))

# Verifica se o índice é válido
if indice_linha < 0 or indice_linha >= len(df_filtrado):
    print("Índice inválido. Saindo do programa.")
    exit()

# Obtém a linha específica do DataFrame
linha_selecionada = df_filtrado.iloc[indice_linha]

cod_rodopar = linha_selecionada['COD. RODOPAR']
doc_rodopar = linha_selecionada['DOCUMENTO RODOPAR']
serie = linha_selecionada['SERIE']
parcela = linha_selecionada['PARCELA']


try:

    query = f"""

    update i set i.lindig = b.lindig

    from pagdoci i

    LEFT OUTER JOIN RODCLI F ON F.codclifor = i.codclifor

    left outer join CargoPoloTemp.dbo.BASEDDA B on b.FORCGC = f.CODCGC and I.DATVEN = B.DATVEN AND i.VLRPAR = B.VLRTIT
    

    where i.codclifor = {cod_rodopar} and i.numdoc = '{doc_rodopar}' and i.SERIE = {serie} and i.numpar = {parcela}

    """

    cursor = conn.cursor()

    cursor.execute(query)

    cursor.commit()

except pyodbc.Error as e:
    print(f"ERRO: {e}")
except Exception as e:
    print(f"ERRO: {e}")
finally:
    # Certifique-se de fechar o cursor após a execução
    cursor.close()

    #doc = 16714
    #linha digitavel = 23790490069049000139401002217709995930000125267
