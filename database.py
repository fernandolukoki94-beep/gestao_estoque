import psycopg2
import os

def inicializar_banco():
    try:
        # Obtém o utilizador atual do Termux automaticamente
        usuario_atual = os.getlogin()

        # Conecta usando o utilizador dinâmico do sistema
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="estoque_db",
            user=usuario_atual,
            port="5432"
        )
        
        cursor = conn.cursor()
        
        # Criação da tabela com sintaxe PostgreSQL
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                quantidade INTEGER NOT NULL,
                preco NUMERIC(10, 2) NOT NULL
            );
        ''')
        
        conn.commit()
        print("Banco de dados PostgreSQL e tabela de produtos inicializados com sucesso!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")

if __name__ == "__main__":
    inicializar_banco()

