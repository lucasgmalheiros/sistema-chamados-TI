from pandas import DataFrame, ExcelWriter, read_sql
from datetime import datetime
from conecta_banco import ConectaBanco


def gera_relatorios_xlsx():
    """Escreve todos os relatórios gerenciais disponíveis em uma tabela do Excel"""
    conn = ConectaBanco()
    date = datetime.now().date()
    queries = queries_relatorios()
    with ExcelWriter(f"relatorios-{date}.xlsx") as writer:
        for query in queries.keys():
            try:
                read_sql(queries[query],conn).to_excel(writer,query)
            except Exception as error:
                print(error)


def queries_relatorios():
    """Retorna todas as consultas disponíveis para fornecer relatórios gerenciais"""
    queries = {
        'ordens_por_servico':"""SELECT	COUNT(*) AS QTD_ORDENS_POR_SERVICO, ID_SERVICO
                                FROM		TB_ORDENS
                                GROUP BY	ID_SERVICO""",

        'ordens_finalizadas':"""SELECT	COUNT(*) AS QTD_ORDENS_FINALIZADAS
                                FROM	TB_ORDENS
                                WHERE	DATA_FIM IS NOT NULL""",

        'ordens_pendentes':"""SELECT	COUNT(*) AS  QTD_ORDENS_PENDENTES
                              FROM		TB_ORDENS 
                              WHERE	    DATA_INICIO IS NULL""",

        'ordens_em_atendimento':"""SELECT	COUNT(*) AS QTD_ORDENS_EM_ATENDIMENTO
                                   FROM		TB_ORDENS 
                                   WHERE	DATA_INICIO IS NOT NULL
                                   AND		DATA_FIM IS NULL""",

        'nota_media_servicos':"""SELECT	    AVG(NOTA) AS NOTA_MEDIA_POR_SERVICO, ID_SERVICO
                                 FROM		TB_ORDENS
                                 WHERE	    DATA_FIM IS NOT NULL
                                 GROUP BY	ID_SERVICO""",

        'nota_media_atendimentos':"""SELECT	    AVG(NOTA) AS NOTA_MEDIA_ATENDIMENTO
                                     FROM	    TB_ORDENS
                                     WHERE	    DATA_FIM IS NOT NULL""",

        'tempo_medio_por_servico':"""SELECT	    AVG(TIMEDIFF(DATA_FIM,DATA_INICIO)) AS T_MEDIO_ATENDIMENTO, ID_SERVICO
                                     FROM		TB_ORDENS
                                     WHERE	    DATA_FIM IS NOT NULL
                                     AND		DATA_INICIO IS NOT NULL
                                     GROUP BY	ID_SERVICO""",

        'tempo_medio_para_atendimento':"""SELECT	AVG(TIMEDIFF(DATA_INICIO,DATA_SOLICITACAO)) AS T_MEDIO_INICIO_ATENDIMENTO, ID_SERVICO
                                          FROM		TB_ORDENS
                                          WHERE	    DATA_INICIO IS NOT NULL
                                          GROUP BY	ID_SERVICO""",

        'qtd_servicos_por_local':"""SELECT      COUNT(*) AS QTD, LOCAL_ATENDIMENTO
                                    FROM		TB_ORDENS
                                    GROUP BY	LOCAL_ATENDIMENTO""",

        'qtd_de_tecnicos_por_cargo':"""SELECT	COUNT(EMAIL) AS QTD, CARGO
                                    FROM		TB_TECNICOS
                                    GROUP BY	CARGO""",

        'lista_de_tecnicos':"""SELECT	NOME, CARGO
                               FROM		TB_TECNICOS""",

        'lista_de_servicos':"""SELECT	NOME, DESCRICAO
                               FROM		TB_SERVICOS""",

        'lista_de_solicitantes':"""SELECT	DISTINCT(EMAIL) AS EMAIL, NOME, CARGO
                                   FROM		TB_SOLICITANTES""",

        'qtd_solicitantes_por_cargo':"""SELECT	COUNT(DISTINCT(EMAIL)) AS QTD, CARGO
                                        FROM		TB_SOLICITANTES
                                        GROUP BY	CARGO"""
        
    }

    return queries
