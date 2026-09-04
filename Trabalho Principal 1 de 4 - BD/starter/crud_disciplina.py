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
    pass


def listar_disciplinas():
    """Devolve a lista de todas as disciplinas, ordenada por codigo."""
    pass


def buscar_disciplina_por_id(id_disciplina):
    """Devolve uma tupla, ou None se nao existir."""
    pass


def atualizar_disciplina(id_disciplina, nome, carga_horaria, periodo):
    """Devolve True se alguma linha foi alterada."""
    pass


def excluir_disciplina(id_disciplina):
    """Devolve True se alguma linha foi removida."""
    pass
