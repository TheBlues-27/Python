"""
crud_aluno.py — Operacoes CRUD da entidade Aluno.

Nenhuma funcao deste arquivo pode usar input() ou print() de menu.
A conversa com o usuario fica toda em main.py.

Regra inegociavel: SEMPRE use ? para os parametros do SQL.
Montar SQL com f-string ou concatenacao (+) zera a questao.
"""

import sqlite3

from database import conectar


# ----------------------------------------------------- CREATE (PRONTO)
def inserir_aluno(matricula, nome, email, data_nascimento):
    """Insere um aluno. Devolve o id gerado ou None se a matricula ja existir."""
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """INSERT INTO aluno (matricula, nome, email, data_nascimento, ativo)
            VALUES (?, ?, ?, ?, 1)"""
    valores = (matricula, nome, email, data_nascimento)
    try:
        cursor.execute(sql, valores)
        conexao.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        cursor.close()
        conexao.close()


# ------------------------------------------------------- READ (PRONTO)
def listar_alunos():
    """Devolve a lista de todos os alunos, ordenada por nome."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""SELECT id, matricula, nome, email, data_nascimento, ativo
                    FROM aluno ORDER BY nome""")
    alunos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return alunos


# --------------------------------------------------------- TODO 3 - DONE
def buscar_aluno_por_id(id_aluno):
    """Devolve uma tupla com os dados do aluno, ou None se nao existir.

    Dica: use fetchone() no lugar de fetchall().
    """
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""SELECT id, matricula, nome, email, data_nascimento, ativo
                    FROM aluno WHERE id = ?""", (id_aluno,))
    aluno = cursor.fetchone()
    cursor.close()
    conexao.close()
    return aluno


# --------------------------------------------------------- TODO 4
def atualizar_aluno(id_aluno, nome, email, data_nascimento):
    """Atualiza nome, email e data de nascimento. Devolve True se mudou algo.

    Dica: UPDATE aluno SET ... WHERE id = ?   (sem o WHERE voce altera TODOS)
    Depois do commit(), cursor.rowcount diz quantas linhas mudaram.
    """
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.executa("""UPDATE aluno SET nome = ?, email = ?, data_nascimento = ?
                    WHERE id = ?""", (nome, email, data_nascimento, id_aluno))
    conexao.commit()
    linhas = cursor.rowcount
    print(f"Linhas alteradas: {linhas}")
    cursor.close()
    conexao.close()


# --------------------------------------------------------- TODO 5
def excluir_aluno(id_aluno):
    """Exclui um aluno pelo id. Devolve True se removeu alguma linha.

    Dica: se o aluno tiver inscricoes, o SQLite levanta sqlite3.IntegrityError.
    Trate a excecao e devolva False nesse caso.
    """
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("""DELETE FROM aluno WHERE id = ?""", (id_aluno,))
        conexao.commit()
        linhas = cursor.rowcount
        print(f"Linhas excluídas: {linhas}")
        cursor.close()
        conexao.close()
    except sqlite3.IntegrityError:
        return False

