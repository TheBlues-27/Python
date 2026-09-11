import sqlite3 as sql

def conectar():
    connect = sql.connect("escola.db")
    execute = connect.execute("PRAGMA foreign_keys = ON")
    return connect

def criar_tabelas():
    connect = conectar()
    cursor = connect.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aluno (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matricula TEXT NOT NULL UNIQUE,
        nome TEXT NOT NULL,
        email TEXT,
        data_nascimento TEXT,
        ativo INTEGER NOT NULL DEFAULT 1
        )""")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disciplina (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL UNIQUE,
            nome TEXT NOT NULL,
            carga_horaria INTEGER NOT NULL,
            periodo INTEGER)
            """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inscricao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL, 
            FOREIGN KEY (aluno_id) REFERENCES aluno(id),
            disciplina_id INTEGER NOT NULL,
            FOREIGN KEY (disciplina_id) REFERENCES disciplina(id),
            nota1 REAL,
            nota2 REAL, 
            UNIQUE(aluno_id, disciplina_id)
            """)
    
    connect.commit()
    cursor.close()
    connect.close()
    
    print("Tabelas foram criadas (ou ja existem) em escola.db.")
    
if __name__ == "__main__":
    criar_tabelas()