import sqlite3 as sql

def connector():
    connect = sql.connect("escola.db")
    execute = connect.execute("PRAGMA foreign_keys = ON")
    return connect

def create_tables():
    connect = connector()
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
            codiogo TEXT NOT NULL UNIQUE,
            nome TEXT NOT NULL,
            carga_horaria INTEGER NOT NULL,
            periodo INTEGER)
            """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inscricao(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL FOREIGN KEY REFERENCES aluno(id),
            disciplina_id INTEGER NOT NULL FOREIGN KEY REFERENCES disciplina(id),
            nota1 REAL,
            nota2 REAL
            UNIQUE(aluno_id, disciplina_id))
            """)
    
    connector.commit()
    cursor.close()
    connector.close()
    
    print("Tabelas foram criadas (ou ja existem) em escola.db.")
    
if __name__ == "__main__":
    create_tables()