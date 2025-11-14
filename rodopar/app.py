import streamlit as st
import pandas as pd
import pyodbc
from datetime import datetime

st.set_page_config(layout='wide')

page_bg_img = """
<style>
[data-testid=stAppViewContainer]{
background-image: linear-gradient(#FFFFFF,#FFFFFF);
}
[data-testid=stSidebar]{
background-image: linear-gradient(#1E3F8E,#1E3F8E);
}
[data-testid=stBaseButton-secondary]{
background-image: linear-gradient(#12239E,#12239E);
}

[data-testid=StyledLinkIconContainer]{
background-image: linear-gradient(#12239E,#12239E);
}
[data-testid=stFileUploaderDropzone]{
background-image: linear-gradient(#12239E,#12239E);
}
[class="st-b3 st-b8 st-bw st-b1 st-bm st-ae st-af st-bn st-ah st-ai st-aj st-bx st-d0"]{
background-image: linear-gradient(#12239E,#12239E);
}
[data-testid="stMainBlockContainer"]{
border-radius: 15px;
background-color: #f9f9f9;
}
[data-testid="stTextInputRootElement"]{
border-radius: 15px;
}

[data-testid="stFileUploaderDropzoneInstructions"]{
color: #000000;
text-align: center;
font-weight: 600; 
}

.titulo-customizado{
color: #000000;
text-align: center;
}
[data-testid="stHeader"]{
background-image: linear-gradient(#1E3F8E,#1E3F8E);
}
[data-testid="stMarkdownContainer"]{
color: #000000;
}
[class="main-svg"]{
style="background: rgb(255, 255, 255, 0);";
}
</style>
"""
st.markdown(page_bg_img,unsafe_allow_html=True)

# Configuração da conexão com o SQL Server
SERVER = '177.47.20.123,1433'
#SERVER = '10.1.1.9'
DATABASE = 'db_visual_rodopar'
USERNAME = 'cyber'
PASSWORD = 'bycyber'
connectionString = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
conn = pyodbc.connect(connectionString)

cursor = conn.cursor()

# Configurando a senha desejada
senha_correta = "123"

# Adicionando um espaço vazio para a mensagem
mensagem_placeholder = st.empty()

senha = st.sidebar.text_input("Digite a senha:", type="password")


# Verificando a senha
if senha == senha_correta:

    # Função principal de leitura e processamento
    def executar(arquivo, sheet):
        try:
            # Lê o arquivo Excel enviado
            df = pd.read_excel(arquivo, sheet_name=sheet)

            # Filtra — mantém apenas os que NÃO são do tipo 'Faturado'
            tipos_excluir = ['Faturado']
            df = df[~df['Fatura'].isin(tipos_excluir)]

            # Seleciona apenas as colunas desejadas
            df = df[['CODFIL', 'SERCON', 'CODCON', 'SALDO', 'CODPAG', 'Fatura']]

            # Ordena por CODPAG e CODFIL
            df = df.sort_values(by=['CODPAG', 'CODFIL'])

            # Definir o nome do arquivo de saída
            output_txt = 'saida.txt'

            # Caminho relativo para o arquivo de saída
            caminho_saida_txt = output_txt

            # Converter e salvar como arquivo de texto
            with open(caminho_saida_txt, 'w') as txt_file:
                for index, row in df.iterrows():
                    txt_file.write(';'.join(map(str, row)) + '\n')

            print(f"Arquivo de texto '{caminho_saida_txt}' criado com sucesso.")
            return df  # ✅ Adiciona isso aqui!

        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")
            return None
        
    def excluir_fatura(fatura):
        fatura = str(fatura)
        try:
            conn = pyodbc.connect(connectionString)
            cursor = conn.cursor()
        except Exception as e:
            print(f"Erro ao conectar-se ao banco: {e}")

        try:
            cursor.execute("""  DELETE FROM RODDUP WHERE NUMDUP = ? """,(fatura))
            cursor.execute("""  DELETE FROM RODIDU WHERE NUMDUP = ? """,(fatura))
            cursor.execute("""  DELETE FROM RECRAT WHERE NUMDUP = ? """,(fatura))
            cursor.execute("""  DELETE FROM RECDOCI WHERE NUMDUP = ? """,(fatura))
            cursor.execute("""  DELETE FROM RECMEN WHERE NUMDUP = ? """,(fatura))
            cursor.execute("""  DELETE FROM RECDOC WHERE NUMDUP = ? """,(fatura))
        
            try:
                # Commit para salvar as alterações
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Erro ao desconectar-se do banco: {e}")

        except Exception as e:
            print(f"Erro ao excluir {e}")


    # ---------------- INTERFACE STREAMLIT ----------------
    aba1, aba2 = st.tabs(["Inserir Fatura","Excluir Fatura"])

    with aba2:
        st.set_page_config(page_title="Exclusão Lançamento Fatura", page_icon="📊")

        numero_fatura = st.text_input("Digite o número da duplicata: (Exemplo: 11066)", "00000")

        if st.button("🔍 Excluir Fatura"):
            excluir_fatura(numero_fatura)

            st.markdown(f"<h4 class='titulo-customizado'>Duplicata: {numero_fatura} excluida!</h4>",unsafe_allow_html = True)
            print(f"Duplicata: {numero_fatura} excluida!")





    with aba1:
        st.set_page_config(page_title="Automação Lançamento Fatura", page_icon="📊")
        

        st.markdown("<h1 class='titulo-customizado'>📊 Contas a Receber - Automação Faturas</h1>",unsafe_allow_html = True)
        st.markdown("<h4 class='titulo-customizado'>Envie o arquivo Excel (.xlsx ou .xlsm) <br> Obs: Certifique-se que o arquivo excel tenha as colunas: <br> [<b>'CODFIL', 'SERCON', 'CODCON', 'SALDO', 'CODPAG', 'Fatura'</b>] <h4>", unsafe_allow_html= True)

        # Cria 3 colunas: esquerda, centro e direita
        col1, col2, col3 = st.columns([1, 2, 1])  # col2 é maior e centraliza os widgets

        # File uploader centralizado
        with col2:
            uploaded_file = st.file_uploader("Selecione o arquivo Excel", type=["xlsx", "xlsm"])

        # Pequeno espaçamento
        st.write("")

        # Text input centralizado
        with col2:
            sheet_name = st.text_input("Digite o nome da planilha (aba):", "Base_Receber")

            if uploaded_file is not None:
                if st.button("🔍 Ler e Processar"):
                    df = executar(uploaded_file, sheet_name)

                    if df is not None:
                        st.success("✅ Planilha processada com sucesso!")
                        st.write(f"Total de linhas processadas: **{len(df)}**")

                        # Exibe o dataframe completo
                        st.dataframe(df)

                        # Função de conversão de data
                        def converter_data(data_str):
                            try:
                                dt = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
                                return dt.strftime("%Y-%m-%d %H:%M")
                            except ValueError:
                                try:
                                    dt = datetime.strptime(data_str, "%d/%m/%Y").replace(hour=0, minute=0, second=0)
                                    return dt.strftime("%Y-%m-%d %H:%M")
                                except ValueError as e:
                                    print(f"Erro ao converter data: {e}")
                                    return None

                        # Função para obter a data e hora atual
                        # def obter_data_hora_atual():
                        #     return datetime.now().strftime("%Y-%m-%d %H:%M")

                        # Função para obter a data e hora atual
                        def obter_data_atual():
                            #return datetime.now().strftime("%Y-%m-%d %H:%M")
                            return datetime.now().strftime("%m-%d-%Y %H:%M:%S")

                        # Função para obter a data e hora atual
                        def obter_apenas_data_atual():
                            return datetime.now().strftime("%m/%d/%Y")

                        # função obter data e hora atual e milisegundos no formato SQL Server
                        def GETDATE():
                            return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

                        # Variáveis auxiliares
                        ultimo_codfil = None
                        ultimo_codpag = None
                        proximo_id = None

                        total = 0

                    # Loop direto sobre o dataframe (substitui leitura de saida.txt)
                        #ABRINDO O ARQUIVO ONDE SE ENCONTRA AS DT COM SEUS DADOS
                        with open('saida.txt','r') as arquivo:
                            for linha in arquivo:
                                codfil = linha.split(';')[0]
                                sercon = linha.split(';')[1]
                                codcon = linha.split(';')[2]
                                saldo = linha.split(';')[3]
                                codpag = linha.split(';')[4]
                                fatura = linha.split(';')[5]

                                #TRATANDO OS DADOS
                                sercon = str(sercon)
                                saldo = float(saldo.replace(',','.'))

                                # somar todos saldo que tiver o mesmo codpag e codfil (em uma variavel) , por exemplo , codfil 5 e codpag 101 deve somar todos os saldos que tiver esses codigos
                                # A variável 'colunas' guardará a lista resultante do split para evitar múltiplos splits da mesma linha
                                total_soma = sum(
                                    float(colunas[3].replace(',', '.')) 
                                    for linha in open('saida.txt', 'r') 
                                    if (colunas := linha.strip().split(';')) and len(colunas) >= 4 and colunas[0] == codfil and colunas[4] == codpag
                                )

                                total_soma = float(total_soma)

                                #print(f"Total soma para codfil {codfil} e codpag {codpag}: {total_soma}")

                                # Chave para identificar se já existe um proximo_id para esse par
                                chave = (codfil, codpag)

                                try:
                                    conn = pyodbc.connect(connectionString)
                                    cursor = conn.cursor()
                                except Exception as e:
                                    print(f"Erro ao conectar-se ao banco: {e}")

                                #PRIMEIRO INSERT
                                try:
                                    # Se for o mesmo codfil e codpag da linha anterior, reutiliza o mesmo proximo_id
                                    if codfil == ultimo_codfil and codpag == ultimo_codpag:
                                        # usa o mesmo proximo_id anterior
                                        pass
                                    else:
                                        total = 0
                                        #PEGANDO ULTIMO ID
                                        cursor.execute("select MAX(NUMDUP) + 1 as MAX_NUMDUP FROM RODDUP")
                                        proximo_id = cursor.fetchone()[0] or 1  # Se não houver registros, use 1 como valor inicial
                                        proximo_id_string = str(proximo_id)

                                        #INSERT NA PRIMEIRA TABELA ()
                                        cursor.execute("""
                                            INSERT INTO RODDUP (USUATU,DATATU,DATINC,USUINC,CODCMO,CODTAR,FATINV,CODFPG,CODCLIFOR,OBSERV,TIPDOC,SEQCON,SEQEND,BOLAVA,CODCLIBOL,OBSER2,CODFIL,CODVEN,CODOPE,CODBCO,NUMDUP,CODTAX,PBASIN,BASINS,VLRINS,ALIINS,DESCAN,VLRPIS,VLRIR,VLRISS,DATVEN,TAXCOB,DESICM,VLRCOR,DATEMI,DESCON,DESCIN,VLRTAX,VLRDUP,VLRLIQ,VLRIND,CODPAD,SITUAC) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

                                            """,(
                                                'HIGOR.MACHADO', obter_data_atual(), obter_data_atual(), 'HIGOR.MACHADO', None, 1707, 'N', None, codpag, None, 'N', None,None, None, codpag, None, codfil,1 , 1 , 237, proximo_id,1,0,0,0,0,0,0,0,0, obter_apenas_data_atual(),0,0,0,obter_data_atual(),0,0,1,0,0,0,1,'I'
                                            ))

                                    #CRIAR UM FOR (SE CODPAG E CODFIL FOR O MESMO, UTILIZAR O MESMO proximo_id) 
                                    cursor.execute("""
                                        INSERT INTO RODIDU VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

                                        """,(
                                            codfil, proximo_id, codfil, codcon,sercon,'CTRC',saldo,'D','S',GETDATE(), GETDATE(), 'HIGOR.MACHADO','I','N',proximo_id_string,saldo,1
                                        ))
                                    
                                    total = total + 1

                                        
                                except Exception as e:
                                    print(f'Erro Primeiro Select {e}')

                                #SEGUNDO UPDATE NA TABELA RODDUP
                                try:
                                    cursor.execute("""
                                                UPDATE RODDUP  SET SITUAC = 'I',DESCAN=ISNULL(DESCAN,0) + 0 WHERE CODFIL=? AND NUMDUP=?
                                                """,(
                                                    codfil, proximo_id
                                                ))

                                except Exception as e:
                                    print(f'Erro Segundo Update {e}')

                                # TERCEIRO UPDATE
                                try:
                                    cursor.execute("""UPDATE RODDUP SET USUATU=?,DATATU=?,CODCMO=?,CODTAR=?,FATINV=?,CODFPG=?,CODCLIFOR=?,OBSERV=?,TIPDOC=?,SEQCON=?,SEQEND=?,BOLAVA=?,CODCLIBOL=?,OBSER2=?,CODVEN=?,CODOPE=?,CODBCO=?,CODTAX=?,PBASIN=?,BASINS=?,VLRINS=?,ALIINS=?,DESCAN=?,VLRPIS=?,VLRIR=?,VLRISS=?,DATVEN=?,TAXCOB=?,DESICM=?,VLRCOR=?,DATEMI=?,DESCON=?,DESCIN=?,VLRTAX=?,VLRDUP=?,VLRLIQ=?,VLRIND=?,CODPAD=?,SITUAC=?  WHERE CODFIL=? AND NUMDUP=?""",(
                                            'HIGOR.MACHADO', obter_data_atual(), None, 1714,'N', None, codpag, None, 'N',None,None, None, codpag, None,1,1,237,1,0,0,0,0,0,0,0,0,obter_apenas_data_atual(),0,0,0,obter_data_atual(),0,0,1,total_soma,total_soma,total_soma,1,'I',codfil, proximo_id

                                    ))

                                    # print(f"valor total é {total_soma} ")

                                except Exception as e:
                                    print(f'Erro Terceiro Update {e}')

                                #ATÉ AQUI TD BEM

                                # # Quarto INSERT
                                # # Se for o mesmo codfil e codpag da linha anterior, reutiliza o mesmo proximo_id
                                # if codfil == ultimo_codfil and codpag == ultimo_codpag:
                                #     # usa o mesmo proximo_id anterior
                                #     pass
                                # else:
                                #     try:
                                #         cursor.execute(""" INSERT INTO RECDOC (NUMDUP,CODFIL, CODPAD, CODCLIFOR, CODVEN, CODBCO, CODOPE, CODTAX, DATEMI, DATVEN, VALDUP, VLRCOM, SITUAC, JURDIA, DESCAN, VLRJUR, VLRCOR, VLRDES, VLRLIQ, VLRREC, REFERE, DATATU, USUATU, ORIGEM, DATINC,USUINC, DESCON, CODFPG, TAXCOB, VLRIND, DESCIN,DATREF) SELECT NUMDUP, CODFIL, CODPAD, CODCLIFOR, CODVEN, CODBCO, CODOPE, CODTAX, DATEMI,  DATVEN, VLRDUP, 0 AS VLRCOM,'I', 0 AS JURDIA, ISNULL(DESCAN, 0) DESCAN, 0 AS VLRJUR, VLRCOR, 0 AS VLRDES, VLRDUP, 0 AS VLRREC, LEFT(OBSERV,255) AS REFERE, GETDATE(), USUATU, 'F', GETDATE(),'HIGOR.MACHADO', ISNULL(DESCON,0) + ISNULL(DESICM, 0) AS DESCON,CODFPG, TAXCOB, VLRIND,DESCIN,DATEMI FROM RODDUP WHERE CODFIL = ? AND NUMDUP = ? """,(
                                #                 codfil, proximo_id

                                #         ))


                                #     except Exception as e:
                                #         print(f'Erro Quarto Update {e}')

                            
                                # # Quinto INSERT
                                # # Se for o mesmo codfil e codpag da linha anterior, reutiliza o mesmo proximo_id
                                # if codfil == ultimo_codfil and codpag == ultimo_codpag:
                                #     # usa o mesmo proximo_id anterior
                                #     pass
                                # else:
                                #     try:
                                #         #PEGANDO ULTIMO ID
                                #         cursor.execute("select MAX(ID_RECDOCI) + 1 as MAX_RECDOCI FROM RECDOCI")
                                #         proximo_recdoci = cursor.fetchone()[0] or 1  # Se não houver registros, use 1 como valor inicial


                                #         cursor.execute("""  INSERT INTO RECDOCI (ID_RECDOCI, NUMDUP, CODFIL, NUMPAR, REFERE, DATVEN, DATREC, SITUAC, VLRPAR, VLRJUR, VLRCOR, VLRDES, VLRLIQ, VLRREC, VLRCOM, DATPRE, TAXCOB, DATATU, USUATU, DATINC, DESCON, VLRIND, DESCIN)  SELECT ? AS ID_RECDOCI,NUMDUP, CODFIL, 1 AS NUMPAR, NULL AS REFERE, ?, NULL AS DATREC, 'D' AS SITUAC, VLRDUP AS VLRPAR, 0 AS VLRJUR, VLRCOR, 0 AS VLRDES, VLRDUP, 0 AS VLRREC, 0 AS VLRCOM, ?  AS DATPRE, TAXCOB, DATATU, USUATU, DATINC, ISNULL(DESCON,0) + ISNULL(DESICM, 0) AS DESCON, VLRIND, ISNULL(DESCIN,0) AS DESCIN FROM RODDUP WHERE CODFIL = ? AND NUMDUP = ? """,(
                                #                 proximo_recdoci, obter_apenas_data_atual(), obter_apenas_data_atual(), codfil, proximo_id

                                #         ))

                                #     except Exception as e:
                                #         print(f'Erro Quinto Update {e}')

                                # # Sexto Delete
                                # try:

                                #     cursor.execute(""" DELETE FROM RECRAT WHERE CODFIL = ? AND NUMDUP = ?
                                #     """,(codfil,proximo_id_string))

                                # except Exception as e:
                                #     print(f'Erro Sexto Delete {e}')


                                #     #armazenar tarrat
                                # # Sétimo insert
                                # try:
                                #     #PEGANDO ULTIMO ID
                                #     cursor.execute("select MAX(ID_RECRAT) + 1 as MAX_RECRAT FROM recrat")
                                #     proximo_id_recrat = cursor.fetchone()[0] or 1  # Se não houver registros, use 1 como valor inicial

                                #     cursor.execute("""SELECT TARRAT.CODUNN, TARRAT.CODCGA, TARRAT.CODCUS, TARRAT.SINTET, TARRAT.ANALIT FROM RODDUP,TARRAT WHERE RODDUP.CODTAR = TARRAT.CODTAR AND CODFIL = ? AND NUMDUP = ?""",(codfil,proximo_id))
                                #     resultado = cursor.fetchone()

                                #     # Verifica se a consulta retornou algum resultado
                                #     if resultado:
                                #         # Desempacota a tupla "resultado" nas cinco variáveis
                                #         cod_unn, cod_cga, cod_cus, sintet, analit = resultado
                                #         cod_cust = str(cod_cus)
                                #         cursor.execute("""    INSERT INTO RECRAT (ID_RECRAT,NUMDUP,CODFIL,CODUNN,CODCGA,CODCUS,SINTET,ANALIT,VALOR,DATATU,USUATU,DATINC,VLRIND) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?) """,(
                                #                 proximo_id_recrat, proximo_id, codfil, cod_unn, cod_cga, cod_cus,sintet,analit,total_soma,GETDATE(),'HIGOR.MACHADO',GETDATE(),total_soma

                                #     ))
                                # except Exception as e:
                                #     print(f'Erro Sétimo Update {e}')

                                # # Oitavo INSERT
                                # try:
                                #     cursor.execute("""    UPDATE RECDOCI SET DATREC =   CASE M.SITUAC       WHEN 'L'   THEN M.DATLAN       ELSE NULL  END  FROM RECDOCI I,RECMEN M  WHERE M.NUMDUP = I.NUMDUP  AND M.CODFIL = I.CODFIL  AND M.NUMPAR = I.NUMPAR  AND  I.CODFIL = ? AND I.NUMDUP = ? AND I.NUMPAR = 1 AND M.NUMLAN = 0 """,(
                                #             codfil, proximo_id_string
                                #     ))

                                # except Exception as e:
                                #     print(f'Erro Oitavo Update {e}')

                                # try:
                                #     cursor.execute("""      UPDATE RECDOCI  SET SITUAC = 'D',   VLRREC= 0 ,VLRJUR= 0 ,VLRDES= 0 ,VLRCOR= 0 ,TAXCOB= 0 ,DESADT= 0 WHERE  CODFIL = ? AND NUMDUP = ? AND NUMPAR = 1 """,(
                                #             codfil, proximo_id_string
                                #     ))

                                # except Exception as e:
                                #     print(f'Erro Nono Update {e}')

                                # try:
                                #     cursor.execute("""   UPDATE RECDOCI SET VLRLIQ = (VLRPAR + VLRJUR + VLRCOR - VLRDES + TAXCOB)   WHERE  CODFIL = ? AND NUMDUP = ? AND NUMPAR = 1""",(
                                #             codfil, proximo_id_string
                                #     ))
                                # except Exception as e:
                                #     print(f'Erro Décimo Update {e}')

                                
                                # # Se for o mesmo codfil e codpag da linha anterior, reutiliza o mesmo proximo_id
                                # if codfil == ultimo_codfil and codpag == ultimo_codpag:
                                #     # usa o mesmo proximo_id anterior
                                #     pass
                                # else:
                                # # Décimo Primeiro insert
                                #     try:
                                #         #PEGANDO ULTIMO ID
                                #         cursor.execute("select MAX(NUMLAN) + 1 as MAX_RECMEN FROM RECMEN")
                                #         proximo_id_recmen = cursor.fetchone()[0] or 1  # Se não houver registros, use 1 como valor inicial


                                #         cursor.execute("""  INSERT INTO RECMEN SELECT ? AS NUMLAN, D.NUMDUP,D.CODFIL, null as NUMPAR, D.CODCLIFOR,  CODTAX AS CODTAX, (SELECT TOP 1 TIPDOC FROM BANTPD ) as TIPDOC, 1 as CODHISRC,null as NUMAVI, null as CODCTA, CODBCO as BANREC, D.CODVEN, 'D' as DebCre, D.VALDUP AS VLRLAN, NULL as DATVEN, DATEMI as DATLAN, 0 AS VLRJUR,0 AS VLRDES, 0 AS VLRCOR, VLRLIQ, 0 AS VLRCOM,D.TAXCOB as TAXCOB,'D' AS SITUAC, left(REFERE,200) as REFERE, ? as DATATU,? AS USUATU,NULL AS ORIGEM,NULL AS DUPDES, NULL AS FILDES, NULL AS DESADT, NULL AS VLRTAX, D.VLRIND AS VLRIND, D.DESCIN AS DESCIN From RECDOC D where CODFIL = ? AND NUMDUP = ? """,(
                                #                 proximo_id_recmen, GETDATE(),'HIGOR.MACHADO', codfil, proximo_id_string
                                #         ))

                                #     except Exception as e:
                                #         print(f'Erro Décimo Primeiro Select {e}')

                                # try:

                                #     cursor.execute("""  UPDATE RECDOC SET SITUAC = 'D',   VLRREC= 0 ,VLRJUR= 0 ,VLRDES= 0 ,VLRCOR= 0 ,DESADT= 0 WHERE CODFIL = ? AND NUMDUP = ?""",(
                                #         codfil, proximo_id_string
                                #     ))

                                #     cursor.execute("""    UPDATE RECDOC SET  VLRLIQ = ISNULL(VALDUP,0) + ISNULL(VLRJUR,0) + ISNULL(VLRCOR,0) - ISNULL(VLRDES,0)  + ISNULL(TAXCOB,0) WHERE CODFIL = ? AND NUMDUP = ?""",(
                                #         codfil, proximo_id_string
                                #     ))

                                #     cursor.execute("""    UPDATE RODIDU SET SITDUP = 'N' WHERE CODFIL = ? AND NUMDUP = ?""",(
                                #         codfil, proximo_id
                                #     ))

                                    
                                #     cursor.execute("""  UPDATE RODDUP SET SITUAC = 'N' WHERE CODFIL = ? AND NUMDUP = ?""",(
                                #         codfil, proximo_id
                                #     ))


                                # except Exception as e:
                                #     print(f'Erro Décimo Segundo Update {e}')

                                # Commit para salvar as alterações
                                conn.commit()

                                ultimo_codfil = codfil
                                ultimo_codpag = codpag

                                if codfil == ultimo_codfil and codpag == ultimo_codpag:
                                    # usa o mesmo proximo_id anterior
                                    pass
                                else:
                                    st.markdown(f"<h4 class='titulo-customizado'>Duplicata: {proximo_id} Dados do Pagador {codpag} inseridos com sucesso! {total} adicionados!</h4>",unsafe_allow_html = True)
                                    print(f"Duplicata: {proximo_id} Dados do Pagador {codpag} inseridos com sucesso! {total} adicionados!")

                                # Atualiza os últimos códigos


                        #FECHAR CONEXÃO APOS TODOS OS INSERTS
                        cursor.close()
                        conn.close()

                        input("\n✅ Todos os dados foram processados com sucesso. Pressione Enter para fechar...")
                        
                        st.markdown("<h4 class='titulo-customizado'>✅ Todos os dados foram processados com sucesso. Pressione Enter para fechar...</h4>",unsafe_allow_html = True)

                    #     # Aqui você colocaria suas ações automatizadas (ex: pyautogui)
                    #     st.text(f"{codfil} | {sercon} | {codcon} | {saldo} | {codpag} | {fatura}")

else:
    st.error("Senha incorreta! Acesso negado.")
