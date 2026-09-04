"""
main.py — Interface de texto (menu) do sistema.

Este arquivo so conversa com o usuario. Toda regra de banco fica nos modulos
database.py, crud_aluno.py e crud_disciplina.py.

O menu de ALUNOS ja tem as opcoes 1 e 2 prontas. Use-as como modelo.
"""

from database import criar_tabelas
from crud_aluno import (inserir_aluno, listar_alunos, buscar_aluno_por_id,
                        atualizar_aluno, excluir_aluno)
from crud_disciplina import (inserir_disciplina, listar_disciplinas,
                             buscar_disciplina_por_id, atualizar_disciplina,
                             excluir_disciplina)


def ler_inteiro(mensagem):
    """Le um numero inteiro do teclado, insistindo ate o usuario acertar."""
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("  Valor invalido. Digite um numero inteiro.")


def menu_alunos():
    while True:
        print("""
--- ALUNOS ---
1) Cadastrar   2) Listar   3) Alterar   4) Excluir   0) Voltar""")
        opcao = input("Opcao: ").strip()

        if opcao == "1":                                   # PRONTO
            matricula = input("Matricula: ").strip()
            nome = input("Nome: ").strip()
            email = input("E-mail: ").strip()
            nascimento = input("Nascimento (AAAA-MM-DD): ").strip()
            if not matricula or not nome:
                print(">> Matricula e nome sao obrigatorios.")
                continue
            novo_id = inserir_aluno(matricula, nome, email, nascimento)
            if novo_id is None:
                print(">> Ja existe aluno com essa matricula.")
            else:
                print(">> Aluno cadastrado com id", novo_id)

        elif opcao == "2":                                 # PRONTO
            alunos = listar_alunos()
            if not alunos:
                print(">> Nenhum aluno cadastrado.")
            for a in alunos:
                print(f"  [{a[0]}] {a[1]} - {a[2]} | {a[3]} | {a[4]}")

        elif opcao == "3":
            # TODO 7: pedir o id, buscar o aluno, avisar se nao existir,
            # ler os novos dados e chamar atualizar_aluno().
            print(">> Ainda nao implementado.")

        elif opcao == "4":
            # TODO 8: pedir o id e chamar excluir_aluno(), tratando o False.
            print(">> Ainda nao implementado.")

        elif opcao == "0":
            return
        else:
            print(">> Opcao invalida.")


def menu_disciplinas():
    # TODO 9: espelhe menu_alunos() para as disciplinas.
    print(">> Ainda nao implementado.")


def main():
    criar_tabelas()
    while True:
        print("""
=== SISTEMA DE REGISTRO ACADEMICO ===
1) Alunos
2) Disciplinas
0) Sair""")
        opcao = input("Opcao: ").strip()
        if opcao == "1":
            menu_alunos()
        elif opcao == "2":
            menu_disciplinas()
        elif opcao == "0":
            print("Ate logo!")
            break
        else:
            print(">> Opcao invalida.")


if __name__ == "__main__":
    main()
