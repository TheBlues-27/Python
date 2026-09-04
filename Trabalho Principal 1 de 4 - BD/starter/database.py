"""
database.py — Camada de acesso ao banco de dados.

Padrao usado em toda a disciplina:
    conectar -> cursor -> execute -> commit -> close

O que ja esta pronto: a funcao conectar() e a tabela aluno.
O que voce precisa fazer: as tabelas disciplina e inscricao.
"""

import sqlite3

NOME_BANCO = "escola.db"


def conectar():
    """Abre e devolve uma conexao com o banco de dados.

    O PRAGMA foreign_keys precisa ser ligado em TODA conexao: por padrao o
    SQLite aceita chaves estrangeiras invalidas silenciosamente.
    """
    conexao = sqlite3.connect(NOME_BANCO)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    # ---------- PRONTO: use este bloco como modelo ----------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aluno (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula       TEXT    NOT NULL UNIQUE,
            nome            TEXT    NOT NULL,
            email           TEXT,
            data_nascimento TEXT,
            ativo           INTEGER NOT NULL DEFAULT 1
        )
    """)

    # ---------- TODO 1: tabela disciplina ----------
    # Colunas: id (PK), codigo (TEXT, NOT NULL, UNIQUE), nome (TEXT, NOT NULL),
    #          carga_horaria (INTEGER, NOT NULL), periodo (INTEGER)
    # cursor.execute(""" ... """)

    # ---------- TODO 2: tabela inscricao (associativa N:N) ----------
    # Colunas: id (PK), aluno_id (FK -> aluno.id), disciplina_id (FK -> disciplina.id),
    #          nota1 (REAL), nota2 (REAL)
    # Nao esqueca: UNIQUE (aluno_id, disciplina_id) — um aluno nao se inscreve
    # duas vezes na mesma disciplina.
    # cursor.execute(""" ... """)

    conexao.commit()
    cursor.close()
    conexao.close()
    print("Tabelas criadas (ou ja existentes) em", NOME_BANCO)


if __name__ == "__main__":
    criar_tabelas()
