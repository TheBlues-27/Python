"""
crud_disciplina.py — Operacoes CRUD da entidade Disciplina.

TODO 6: implemente as cinco funcoes abaixo, espelhando crud_aluno.py.
Se a estrutura ficar identica, voce fez certo: previsibilidade e reuso sao
principios do RAD.
"""

import sqlite3

from database import conectar


def inserir_disciplina(codigo, nome, carga_horaria, periodo):
    """Devolve o id gerado ou None se o codigo ja existir."""
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""INSERT INTO disciplina (codigo, nome, carga_horaria, periodo)
                        VALUES (?, ?, ?, ?)""", (codigo, nome, carga_horaria, periodo,))
        conexao.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None                
    finally:
        cursor.close()
        conexao.close()

def listar_disciplinas():
    """Devolve a lista de todas as disciplinas, ordenada por codigo."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""SELECT * FROM disciplina ORDER BY codigo""")
    disciplinas = cursor.fetchall()
    cursor.close()
    conexao.close()
    return disciplinas


def buscar_disciplina_por_id(id_disciplina):
    """Devolve uma tupla, ou None se nao existir."""
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""SELECT * FROM disciplina WHERE id = ?""", (id_disciplina,))
        return cursor.fetchone()
    except sqlite3.IntegrityError:
        return None
    finally:
        cursor.close()
        conexao.close()



def atualizar_disciplina(id_disciplina, nome, carga_horaria, periodo):
    """Devolve True se alguma linha foi alterada."""
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""UPDATE disciplina SET nome = ?, carga_horaria = ?, periodo = ?
                        WHERE id = ?""", (nome, carga_horaria, periodo, id_disciplina))
        linhas = cursor.rowcount
        conexao.commit()
        return linhas > 0
    finally:
        cursor.close()
        conexao.close()



def excluir_disciplina(id_disciplina):
    """Devolve True se alguma linha foi removida."""
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""DELETE FROM disciplina WHERE id = ?""", (id_disciplina,))
        linhas = cursor.rowcount
        conexao.commit()
        return linhas > 0
    except sqlite3.IntegrityError:
        return False
    finally:
        cursor.close()
        conexao.close()
