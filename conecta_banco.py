# coding=utf-8
import mysql.connector


# Conexão com banco de dados
def ConectaBanco():
    """Ligação com banco de dados MySQL, inserir seu usuário e senha"""
    cnx = mysql.connector.connect(database='PROJETO_DEP', host='localhost', user='root', passwd='password')
    cnx.autocommit = True
    return cnx
