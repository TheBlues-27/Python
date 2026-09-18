"""
autoteste.py — Rode ANTES de entregar.

Este script cria um banco temporario, exercita todas as funcoes que voce
implementou e diz o que passou e o que falhou. Ele NAO mexe no seu escola.db.

Uso:
    python autoteste.py

Atencao: passar em todos os testes nao garante nota cheia (a rubrica avalia
tambem o modelo de dados, o README e a organizacao do codigo), mas falhar em
algum teste garante que ha algo quebrado.
"""

import os
import sqlite3
import sys

import database

BANCO_TESTE = "_autoteste.db"

aprovados = 0
reprovados = 0


def checar(descricao, condicao, dica=""):
    global aprovados, reprovados
    if condicao:
        aprovados += 1
        print(f"  [OK]    {descricao}")
    else:
        reprovados += 1
        print(f"  [FALHA] {descricao}")
        if dica:
            print(f"          -> {dica}")


def colunas_da_tabela(nome_tabela):
    conexao = database.conectar()
    cursor = conexao.cursor()
    cursor.execute(f"PRAGMA table_info({nome_tabela})")
    colunas = [linha[1] for linha in cursor.fetchall()]
    cursor.close()
    conexao.close()
    return colunas


def main():
    global reprovados

    # Redireciona o modulo para um banco descartavel
    database.NOME_BANCO = BANCO_TESTE
    if os.path.exists(BANCO_TESTE):
        os.remove(BANCO_TESTE)

    import crud_aluno
    import crud_disciplina

    print("\n=== 1. Estrutura do banco ===")
    database.criar_tabelas()
    checar("tabela aluno existe", "nome" in colunas_da_tabela("aluno"))
    checar("tabela disciplina existe", "codigo" in colunas_da_tabela("disciplina"),
           "TODO 1 em database.py")
    checar("tabela inscricao existe", "aluno_id" in colunas_da_tabela("inscricao"),
           "TODO 2 em database.py")

    print("\n=== 2. CRUD de Aluno ===")
    id_a = crud_aluno.inserir_aluno("999001", "Fulano Teste", "f@x.br", "2000-05-05")
    checar("inserir_aluno devolve um id", isinstance(id_a, int))

    repetido = crud_aluno.inserir_aluno("999001", "Outro", "o@x.br", "2001-01-01")
    checar("matricula duplicada e recusada (devolve None)", repetido is None,
           "trate sqlite3.IntegrityError no insert")

    lista = crud_aluno.listar_alunos()
    checar("listar_alunos devolve 1 registro", lista is not None and len(lista) == 1)

    achado = crud_aluno.buscar_aluno_por_id(id_a)
    checar("buscar_aluno_por_id encontra o aluno",
           achado is not None and "Fulano" in str(achado), "TODO 3")

    checar("buscar_aluno_por_id devolve None para id inexistente",
           crud_aluno.buscar_aluno_por_id(999999) is None, "use fetchone()")

    checar("atualizar_aluno devolve True",
           crud_aluno.atualizar_aluno(id_a, "Fulano Alterado", "f2@x.br", "2000-05-05") is True,
           "TODO 4 — devolva cursor.rowcount > 0")

    depois = crud_aluno.buscar_aluno_por_id(id_a)
    checar("o nome mudou de fato no banco", "Alterado" in str(depois),
           "faltou conexao.commit()?")

    checar("atualizar_aluno devolve False para id inexistente",
           crud_aluno.atualizar_aluno(999999, "X", "x@x.br", "2000-01-01") is False)

    print("\n=== 3. CRUD de Disciplina ===")
    id_d = crud_disciplina.inserir_disciplina("ARA0095", "RAD em Python", 80, 4)
    checar("inserir_disciplina devolve um id", isinstance(id_d, int), "TODO 6")
    checar("codigo duplicado e recusado",
           crud_disciplina.inserir_disciplina("ARA0095", "Copia", 80, 4) is None)
    checar("listar_disciplinas devolve 1 registro",
           crud_disciplina.listar_disciplinas() is not None
           and len(crud_disciplina.listar_disciplinas()) == 1)
    checar("buscar_disciplina_por_id encontra",
           crud_disciplina.buscar_disciplina_por_id(id_d) is not None)
    checar("atualizar_disciplina devolve True",
           crud_disciplina.atualizar_disciplina(id_d, "RAD", 40, 5) is True)

    print("\n=== 4. Integridade referencial ===")
    conexao = database.conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO inscricao (aluno_id, disciplina_id) VALUES (?, ?)",
                   (id_a, id_d))
    conexao.commit()
    cursor.close()
    conexao.close()

    checar("aluno com inscricao NAO pode ser excluido",
           crud_aluno.excluir_aluno(id_a) is False,
           "ligue PRAGMA foreign_keys e trate IntegrityError — TODO 5")

    conexao = database.conectar()
    conexao.execute("DELETE FROM inscricao")
    conexao.commit()
    conexao.close()

    checar("aluno sem inscricao pode ser excluido",
           crud_aluno.excluir_aluno(id_a) is True)
    checar("excluir id inexistente devolve False",
           crud_aluno.excluir_aluno(999999) is False)
    checar("excluir_disciplina funciona",
           crud_disciplina.excluir_disciplina(id_d) is True)

    print("\n=== 5. Seguranca do SQL ===")
    fonte = ""
    for arquivo in ("crud_aluno.py", "crud_disciplina.py"):
        with open(arquivo, encoding="utf-8") as f:
            fonte += f.read()
    suspeito = ('f"""SELECT' in fonte or 'f"SELECT' in fonte
                or 'f"INSERT' in fonte or 'f"""INSERT' in fonte
                or 'f"UPDATE' in fonte or 'f"DELETE' in fonte)
    checar("nenhum SQL montado com f-string", not suspeito,
           "use ? e passe uma tupla de valores")

    os.remove(BANCO_TESTE)
    print(f"\n---------------------------------------")
    print(f"  {aprovados} OK   /   {reprovados} FALHA(S)")
    print(f"---------------------------------------\n")
    sys.exit(1 if reprovados else 0)


if __name__ == "__main__":
    try:
        main()
    except Exception as erro:
        print("\n!! O autoteste parou com um erro:", type(erro).__name__, "-", erro)
        print("!! Provavelmente ha uma funcao ainda com 'pass' ou um TODO pendente.")
        if os.path.exists(BANCO_TESTE):
            os.remove(BANCO_TESTE)
        sys.exit(1)
