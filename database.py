import sqlite3

def inicializar_banco():
    # Conecta ao arquivo do banco de dados (se não existir, ele cria)
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    
    # Cria a tabela de produtos utilizando comandos SQL puros
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL
        )
    ''')
    
    conexao.commit()
    conexao.close()
    print("Banco de dados e tabela de produtos criados com sucesso!")

if __name__ == '__main__':
    inicializar_banco()

