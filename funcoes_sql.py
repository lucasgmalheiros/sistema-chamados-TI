# coding=utf-8
import mysql.connector
from conecta_banco import ConectaBanco


# ----------------------------------------- Geral --------------------------------------------#

def InsertSolicitante(email, senha, nome, cargo):
    """Cadastra usuários nas tabelas de solicitantes e de técnicos de informática"""
    execute = True
    cnx = ConectaBanco()
    cursor = cnx.cursor()

    sql = f"INSERT INTO TB_SOLICITANTES VALUES ('{email}', '{senha}', '{nome}', '{cargo}')"

    try:
        cursor.execute(sql)
    except mysql.connector.Error as err:
        print(f"Erro: {err.errno} - {err.msg}")
        execute = False

    cnx.close()
    return execute


def InsertTecnico(email, senha, nome, cargo):
    """Cadastra usuários nas tabelas de solicitantes e de técnicos de informática"""
    execute = True
    cnx = ConectaBanco()
    cursor = cnx.cursor()

    sql = f"INSERT INTO TB_TECNICOS VALUES ('{email}', '{senha}', '{nome}', '{cargo}')"

    try:
        cursor.execute(sql)
    except mysql.connector.Error as err:
        print(f"Erro: {err.errno} - {err.msg}")
        execute = False

    cnx.close()
    return execute


def InsertOrdem(email, categoria, comentario, prioridade, local):
    """Cadastra uma ordem na tabela de ordens"""
    execute = True
    cnx = ConectaBanco()
    cursor = cnx.cursor()

    sql = f"""
            INSERT INTO TB_ORDENS (ID_SERVICO, EMAIL_SOLICITANTE, DATA_SOLICITACAO, DESCRIÇÃO,
            URGENCIA, LOCAL_ATENDIMENTO) VALUES ((SELECT ID_SERVICO FROM TB_SERVICOS WHERE NOME =
            '{categoria}'), '{email}', NOW(), '{comentario}', {prioridade}, '{local}');
           """
    try:
        cursor.execute(sql)
    except mysql.connector.Error as err:
        print(f"Erro: {err.errno} - {err.msg}")
        execute = False

    cnx.close()
    return execute


def CheckLogin(email, senha):
    """Avalia se o email e senha fornecidos estão cadastrados nas tabelas
    de solicitantes ou tecnicos. Retorna o cargo referente ao login e a tabela em que se encontra."""
    cargo = 'Usuário não cadastrado'
    tabela = None

    cnx = ConectaBanco()
    cursor = cnx.cursor()

    try:
        # Tenta buscar na tabela de solicitantes
        consulta = f"SELECT CARGO FROM TB_SOLICITANTES WHERE EMAIL='{email}' AND SENHA = '{senha}'"
        cursor.execute(consulta)
        dados = cursor.fetchall()
        if len(dados) != 0:
            cargo = dados[0][0]
            tabela = 'TB_SOLICITANTES'
        # Caso não encontre
        else:
            # Tenta busca na tabela de tecnicos de informatica
            try:
                consulta = f"SELECT CARGO FROM TB_TECNICOS WHERE EMAIL='{email}' AND SENHA = '{senha}'"
                cursor.execute(consulta)
                dados = cursor.fetchall()
                if len(dados) != 0:
                    cargo = dados[0][0]
                    tabela = 'TB_TECNICOS'
            except mysql.connector.Error as err:
                print(f"Erro: {err.errno} - {err.msg}")
    except mysql.connector.Error as err:
        print(f"Erro: {err.errno} - {err.msg}")

    cnx.close()
    return cargo, tabela


def ListaServicos():
    """Apresenta a lista de todos os serviços prestados pelo setor de informática em ordem alfabética"""
    lista = []
    cnx = ConectaBanco()
    cursor = cnx.cursor()
    sql = "SELECT DISTINCT NOME FROM TB_SERVICOS"
    cursor.execute(sql)
    servicos = cursor.fetchall()
    for item in servicos:
        lista.append(item[0])
    cnx.close()
    return sorted(lista)


# ----------------------------------------- Solicitante --------------------------------------------#

def SelectChamadoEmFilaSolicitante(email):
    """Apresenta todos os chamados efetuados mas não concluídos para um determinado solicitante"""
    cnx = ConectaBanco()
    cursor = cnx.cursor()
    ordens = []
    # Seleciona apenas os chamados não concluídos, em que data_fim é nula
    sql = f"""
           SELECT S.NOME, DATE(O.DATA_INICIO), O.EMAIL_SOLICITANTE, 
           (SELECT AVG(TIMESTAMPDIFF(MINUTE, DATA_SOLICITACAO, DATA_FIM)) AS TEMPO_MEDIO
           FROM TB_ORDENS WHERE ID_SERVICO=O.ID_SERVICO) AS T_MEDIO, ID_ORDEM
           FROM TB_SERVICOS AS S,TB_ORDENS AS O
           WHERE O.ID_SERVICO = S.ID_SERVICO
           AND DATA_FIM IS NULL
           ORDER BY O.URGENCIA DESC, O.DATA_SOLICITACAO ASC
           """
    try:
        cursor.execute(sql)
        c = cursor.fetchall()
        count = 1
        for ordem in c:
            o = list(ordem)
            o.append(count)
            ordens.append(o)
            count += 1
        # Filtra por email solicitante
        ordens_temp = ordens.copy()
        ordens = []
        for ordem in ordens_temp:
            if ordem[2] == email:
                ordens.append(ordem)
        # Manipula saídas
        for ordem in ordens:
            # Remove o e-mail
            ordem.pop(2)
            # Transforma tempo médio para float
            if ordem[2] is not None:
                ordem[2] = float(ordem[2])
            # Caso não haja tempo de início o chamado está em fila
            if ordem[1] is None:
                ordem[1] = 'Em fila'
            else:
                ordem[1] = 'Em atendimento'

    except mysql.connector.Error as err:
        print(f"Erro: {err.errno} - {err.msg}")
    cnx.close()
    return ordens


def SelectChamadoConcluidoSolicitante(email):
    """Apresenta todos os chamados efetuados e concluídos para um determinado solicitante"""
    cnx = ConectaBanco()
    cursor = cnx.cursor()
    concluidos = []
    sql = f"""
          SELECT TB_SERVICOS.NOME, DATE(TB_ORDENS.DATA_FIM), TB_TECNICOS.NOME AS RESP_TEC, 
          TIMESTAMPDIFF(MINUTE, DATA_SOLICITACAO, DATA_FIM) AS TEMPO_EXEC, ID_ORDEM FROM TB_SERVICOS,  
          TB_ORDENS, TB_TECNICOS WHERE TB_SERVICOS.ID_SERVICO = TB_ORDENS.ID_SERVICO AND 
          TB_ORDENS.EMAIL_TECNICO = TB_TECNICOS.EMAIL AND TB_ORDENS.EMAIL_SOLICITANTE = '{email}'
          ORDER BY DATA_FIM ASC
          """
    try:
        cursor.execute(sql)
        concluidos = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Erro: {err.errno} - {err.msg}")
    cnx.close()
    return concluidos


def UpdateFeedbackSolicitante(id_ordem, feedback, nota):
    """Insere o feedback do solicitante no local correspondente na tabela de ordens"""
    execute = True
    cnx = ConectaBanco()
    cursor = cnx.cursor()
    sql = f"UPDATE TB_ORDENS SET NOTA = {nota}, FEEDBACK = '{feedback}' WHERE ID_ORDEM = {id_ordem}"

    try:
        cursor.execute(sql)
    except mysql.connector.Error as err:
        print(f"Erro: {err.errno} - {err.msg}")
        execute = False
    cnx.close()
    return execute


# -------------------------------------------- Tecnico -----------------------------------------------#
def SelectChamadosEmFilaTecnico():
    """Apresenta todos os chamados não concluídos"""
    cnx = ConectaBanco()
    cursor = cnx.cursor()
    ordens = []
    # Seleciona apenas os chamados não concluídos, em que data_fim é nula
    sql = f"""
            SELECT S.NOME, DATE(O.DATA_INICIO), O.URGENCIA,
           (SELECT AVG(TIMESTAMPDIFF(MINUTE, DATA_SOLICITACAO, DATA_FIM)) AS TEMPO_MEDIO
           FROM TB_ORDENS WHERE ID_SERVICO=O.ID_SERVICO) AS T_MEDIO, O.ID_ORDEM, O.LOCAL_ATENDIMENTO
           FROM TB_SERVICOS AS S,TB_ORDENS AS O
           WHERE O.ID_SERVICO = S.ID_SERVICO
           AND DATA_FIM IS NULL
           ORDER BY O.URGENCIA DESC, O.DATA_SOLICITACAO ASC
               """
    try:
        cursor.execute(sql)
        c = cursor.fetchall()
        count = 1
        for ordem in c:
            o = list(ordem)
            o.append(count)
            ordens.append(o)
            count += 1
        for ordem in ordens:
            # Transforma tempo médio para float
            if ordem[3] is not None:
                ordem[3] = float(ordem[3])
            # Caso não haja tempo de início o chamado está em fila
            if ordem[1] is None:
                ordem[1] = 'Em fila'
            else:
                ordem[1] = 'Em atendimento'
            # Decodifica urgencia
            if ordem[2] == 1 or ordem[2] == 0:
                ordem[2] = 'Baixa'
            elif ordem[2] == 2:
                ordem[2] = 'Média'
            else:
                ordem[2] = 'Alta'

    except mysql.connector.Error as err:
        print(f"Erro: {err.errno} - {err.msg}")
    cnx.close()
    return ordens


def SelectDescricaoChamadoTecnico(id_ordem):
    """Dada uma ordem de serviço, mostra ao técnico de informática informações relevantes inseridas pelo solicitante"""
    cnx = ConectaBanco()
    cursor = cnx.cursor()
    sql = f"""SELECT DESCRIÇÃO, URGENCIA, LOCAL_ATENDIMENTO, TB_SERVICOS.NOME AS SERVICO, 
              TB_SOLICITANTES.NOME, TB_SOLICITANTES.CARGO, DATE(TB_ORDENS.DATA_INICIO)
              FROM TB_ORDENS, TB_SERVICOS, TB_SOLICITANTES
              WHERE ID_ORDEM = {id_ordem} AND TB_ORDENS.ID_SERVICO = TB_SERVICOS.ID_SERVICO 
              AND TB_ORDENS.EMAIL_SOLICITANTE = TB_SOLICITANTES.EMAIL"""
    cursor.execute(sql)
    chamados = cursor.fetchall()
    chamados = [list(i) for i in chamados]
    urgencia = chamados[0][1]
    if urgencia == 1 or urgencia == 0:
        chamados[0][1] = 'Baixa'
    elif urgencia == 2:
        chamados[0][1] = 'Média'
    else:
        chamados[0][1] = 'Alta'
    # Caso não haja tempo de início o chamado está em fila
    if chamados[0][-1] is None:
        chamados[0][-1] = 'Em fila'
    else:
        chamados[0][-1] = 'Em atendimento'
    cnx.close()
    return chamados[0]


def UpdateOrdemTecnico(descricao, prioridade, local, id_ordem):
    """Atualiza a ordem com os novos dados inseridos pelo técnico de informática"""
    execute = True
    cnx = ConectaBanco()
    cursor = cnx.cursor()
    sql = f"""UPDATE PROJETO_DEP.TB_ORDENS SET DESCRIÇÃO = '{descricao}', URGENCIA = {prioridade}, 
             LOCAL_ATENDIMENTO = '{local}' WHERE ID_ORDEM = {id_ordem}"""
    try:
        cursor.execute(sql)
    except mysql.connector.Error as err:
        print(f"Erro: {err.errno} - {err.msg}")
        execute = False
    cnx.close()
    return execute


def SelectChamadoConcluidoTecnico():
    """Apresenta todos os chamados já concluídos registrados no sistema"""
    cnx = ConectaBanco()
    cursor = cnx.cursor()
    concluidos = []
    sql = f"""
              SELECT TB_SERVICOS.NOME, DATE(TB_ORDENS.DATA_FIM), TB_TECNICOS.NOME AS RESP_TEC, 
              TIMESTAMPDIFF(MINUTE, DATA_SOLICITACAO, DATA_FIM) AS TEMPO_EXEC, ID_ORDEM FROM TB_SERVICOS,  
              TB_ORDENS, TB_TECNICOS WHERE TB_SERVICOS.ID_SERVICO = TB_ORDENS.ID_SERVICO AND 
              TB_ORDENS.EMAIL_TECNICO = TB_TECNICOS.EMAIL
              ORDER BY DATA_FIM ASC
              """
    try:
        cursor.execute(sql)
        concluidos = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Erro: {err.errno} - {err.msg}")
    cnx.close()
    return concluidos


def SelectChamadosFeedbackTecnico(id_ordem):
    """Apresenta o feedback dos serviços realizados pelos técnicos"""
    cnx = ConectaBanco()
    cursor = cnx.cursor()
    sql = f"""SELECT DESCRIÇÃO, LOCAL_ATENDIMENTO, TB_SERVICOS.NOME AS SERVICO, 
              TB_SOLICITANTES.NOME, TB_SOLICITANTES.CARGO, TB_ORDENS.DATA_FIM, TB_TECNICOS.NOME, NOTA, FEEDBACK
              FROM TB_ORDENS, TB_SERVICOS, TB_SOLICITANTES, TB_TECNICOS
              WHERE ID_ORDEM = {id_ordem} 
              AND TB_ORDENS.ID_SERVICO = TB_SERVICOS.ID_SERVICO 
              AND TB_ORDENS.EMAIL_SOLICITANTE = TB_SOLICITANTES.EMAIL
              AND TB_ORDENS.EMAIL_TECNICO = TB_TECNICOS.EMAIL"""
    cursor.execute(sql)
    chamados = cursor.fetchall()
    chamados = [list(i) for i in chamados]
    cnx.close()
    return chamados[0]


def UpdateAtendeChamadoTecnico(id_ordem, status, email_tecnico):
    """Atualiza o status do chamado quando o técnico de informática
    utiliza a funcionalidade de atender chamado"""
    execute = True
    cnx = ConectaBanco()
    cursor = cnx.cursor()
    sql = '_'
    if status == "Em fila":
        sql = f"""
            UPDATE projeto_dep.tb_ordens
            SET EMAIL_TECNICO = '{email_tecnico}', DATA_INICIO = NOW()
            WHERE ID_ORDEM = {id_ordem}
            """
    elif status == "Em atendimento":
        sql = f"""
            UPDATE projeto_dep.tb_ordens
            SET EMAIL_TECNICO = '{email_tecnico}', DATA_FIM = NOW(), URGENCIA = -1 
            WHERE ID_ORDEM = {id_ordem}
            """
    try:
        cursor.execute(sql)
    except mysql.connector.Error as err:
        print(f"Erro: {err.errno} - {err.msg}")
        execute = False
    cnx.close()
    return execute


# -------------------------------------------- Coordenador -----------------------------------------------#
def Relatorio(opcao):
    """Realiza uma consulta no banco de dados de acordo com a opção escolhida
    pelo coordenador de informática, permitindo a apresentação dos relatórios"""
    cnx = ConectaBanco()
    cursor = cnx.cursor()
    sql = '_'
    dados = []
    # 1 - Quantidade total de ordens por serviço
    if opcao == 1:
        sql = f"""SELECT TB_SERVICOS.NOME AS SERVICO, COUNT(TB_ORDENS.ID_ORDEM) AS N_SOLICITACOES 
                  FROM TB_ORDENS , TB_SERVICOS
                  WHERE TB_SERVICOS.ID_SERVICO = TB_ORDENS.ID_SERVICO
                  GROUP BY TB_ORDENS.ID_SERVICO
                  ORDER BY TB_SERVICOS.NOME
               """
    # 2 - Tempo médio por funcionário
    elif opcao == 2:
        sql = """
              SELECT TB_TECNICOS.NOME, AVG(TIMESTAMPDIFF(MINUTE,DATA_SOLICITACAO,DATA_FIM)) AS T_MEDIO_ATENDIMENTO 
              FROM TB_ORDENS, TB_TECNICOS 
              WHERE DATA_INICIO IS NOT NULL
              AND DATA_FIM IS NOT NULL
              AND TB_TECNICOS.EMAIL = TB_ORDENS.EMAIL_TECNICO
              GROUP BY TB_TECNICOS.EMAIL
              """
    # 3 - Quantidade de chamados em aberto por serviço
    elif opcao == 3:
        sql = """
              SELECT TB_SERVICOS.NOME , COUNT(*) AS QTD
              FROM TB_ORDENS, TB_SERVICOS
              WHERE DATA_FIM IS  NULL	
              AND TB_SERVICOS.ID_SERVICO = TB_ORDENS.ID_SERVICO
              GROUP BY TB_ORDENS.ID_SERVICO
              ORDER BY TB_SERVICOS.NOME
              """
    # 4 - Tempo médio por cargo do solicitante
    elif opcao == 4:
        sql = """
              SELECT TB_SOLICITANTES.CARGO, AVG(TIMESTAMPDIFF(MINUTE,DATA_SOLICITACAO,DATA_FIM)) AS T_MEDIO_ATENDIMENTO 
              FROM TB_ORDENS, TB_SOLICITANTES WHERE DATA_INICIO IS NOT NULL	
              AND DATA_FIM IS NOT NULL
              AND TB_SOLICITANTES.EMAIL = TB_ORDENS.EMAIL_SOLICITANTE
              GROUP BY TB_SOLICITANTES.CARGO;
              """
    # 5 - Tempo médio de atendimento por tipo de serviço
    elif opcao == 5:
        sql = """
              SELECT TB_SERVICOS.NOME, AVG(TIMESTAMPDIFF(MINUTE,DATA_SOLICITACAO,DATA_FIM)) AS T_MEDIO_ATENDIMENTO 
              FROM TB_ORDENS,tb_servicos WHERE DATA_INICIO IS NOT NULL	
              AND DATA_FIM IS NOT NULL
              AND TB_SERVICOS.ID_SERVICO = TB_ORDENS.ID_SERVICO
              GROUP BY TB_ORDENS.ID_SERVICO
              ORDER BY TB_SERVICOS.NOME DESC
              """
    try:
        cursor.execute(sql)
        dados = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Erro: {err.errno} - {err.msg}")
    cnx.close()
    return dados


# -------------------------- Roda tudo -------------------------------#
if __name__ == '__main__':
    print(Relatorio(5))
