"""
seed.py — Carga de dados de exemplo.

Rode este script uma vez, depois de criar as tabelas, para ter dados com que
testar as telas sem precisar digitar tudo a cada execucao.

ATENCAO: este script so roda ate o fim depois que voce concluir os TODOs 1, 2
e 6 (tabelas disciplina e inscricao + CRUD de disciplina). Antes disso ele vai
falhar — e isso e esperado.
"""

from database import criar_tabelas, conectar
from crud_aluno import inserir_aluno, listar_alunos
from crud_disciplina import inserir_disciplina, listar_disciplinas

ALUNOS = [
    ("202501001", "Ana Beatriz Ramos",  "ana.ramos@exemplo.edu.br",  "2004-03-12"),
    ("202501002", "Bruno Carvalho",     "bruno.c@exemplo.edu.br",    "2003-11-02"),
    ("202501003", "Carla Menezes",      "carla.m@exemplo.edu.br",    "2005-07-25"),
    ("202501004", "Diego Nakamura",     "diego.n@exemplo.edu.br",    "2002-01-18"),
    ("202501005", "Elisa Torres",       "elisa.t@exemplo.edu.br",    "2004-09-30"),
]

DISCIPLINAS = [
    ("ARA0095", "Desenvolvimento Rapido de Aplicacoes em Python", 80, 4),
    ("ARA0039", "Banco de Dados",                                 80, 3),
    ("ARA0017", "Engenharia de Software",                          40, 5),
    ("ARA0062", "Estrutura de Dados",                              80, 3),
]

INSCRICOES = [
    # (matricula_do_aluno, codigo_da_disciplina, nota1, nota2)
    ("202501001", "ARA0095", 8.5, 9.0),
    ("202501001", "ARA0039", 7.0, 6.5),
    ("202501002", "ARA0095", 5.0, 4.5),
    ("202501003", "ARA0095", 9.5, 10.0),
    ("202501003", "ARA0017", 8.0, None),
    ("202501004", "ARA0062", 6.0, 7.5),
]


def popular():
    criar_tabelas()

    for matricula, nome, email, nascimento in ALUNOS:
        if inserir_aluno(matricula, nome, email, nascimento) is None:
            print("  (ja existia) aluno", matricula)

    for codigo, nome, carga, periodo in DISCIPLINAS:
        if inserir_disciplina(codigo, nome, carga, periodo) is None:
            print("  (ja existia) disciplina", codigo)

    # As inscricoes precisam do id interno, nao da matricula/codigo.
    mapa_alunos = {a[1]: a[0] for a in listar_alunos()}
    mapa_disciplinas = {d[1]: d[0] for d in listar_disciplinas()}

    conexao = conectar()
    cursor = conexao.cursor()
    for matricula, codigo, nota1, nota2 in INSCRICOES:
        try:
            cursor.execute(
                """INSERT INTO inscricao (aluno_id, disciplina_id, nota1, nota2)
                   VALUES (?, ?, ?, ?)""",
                (mapa_alunos[matricula], mapa_disciplinas[codigo], nota1, nota2))
        except Exception as erro:
            print("  (ignorado)", matricula, codigo, "->", erro)
    conexao.commit()
    cursor.close()
    conexao.close()

    print(f"Carga concluida: {len(listar_alunos())} alunos e "
          f"{len(listar_disciplinas())} disciplinas no banco.")


if __name__ == "__main__":
    popular()
