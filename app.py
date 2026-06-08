from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)

def conectar_banco():
    # Obtém o utilizador atual do sistema automaticamente
    usuario_atual = os.getlogin()
    
    # Conecta ao PostgreSQL. Usamos RealDictCursor para que o retorno 
    # seja em formato de dicionário pronto para virar JSON, igual ao sqlite3.Row
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="estoque_db",
        user=usuario_atual,
        port="5432",
        cursor_factory=RealDictCursor
    )
    return conn

# 1. Validação de Dados (Melhoria de Segurança)
def validar_produto(dados):
    if not dados or 'nome' not in dados or 'quantidade' not in dados or 'preco' not in dados:
        return False
    if not dados['nome'].strip(): # Evita nomes vazios ou só com espaços
        return False
    if not isinstance(dados['quantidade'], int) or dados['quantidade'] < 0:
        return False
    if not isinstance(dados['preco'], (int, float)) or dados['preco'] < 0:
        return False
    return True

# Rota POST - Criar Produto (Com tratamento de erros)
@app.route('/produtos', methods=['POST'])
def adicionar_produto():
    dados = request.get_json()
    if not validar_produto(dados):
        return jsonify({"erro": "Dados inválidos. Verifique os campos, valores e tipos."}), 400
    
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        # No PostgreSQL usamos RETURNING id para pegar o ID gerado pelo SERIAL
        cursor.execute(
            'INSERT INTO produtos (nome, quantidade, preco) VALUES (%s, %s, %s) RETURNING id',
            (dados['nome'], dados['quantidade'], dados['preco'])
        )
        id_gerado = cursor.fetchone()['id']
        
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"id": id_gerado, "mensagem": "Produto adicionado com sucesso!"}), 201
        
    except Exception as e:
        return jsonify({"erro": f"Erro interno no servidor: {str(e)}"}), 500

# Rota GET - Listar Todos os Produtos (Simplificada e limpa)
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM produtos')
        produtos = cursor.fetchall() # Já vem como lista de dicionários por causa do RealDictCursor
        
        cursor.close()
        conn.close()
        return jsonify(produtos), 200
        
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar produtos: {str(e)}"}), 500

# Rota GET - Buscar Produto Específico por ID (Nova Funcionalidade)
@app.route('/produtos/<int:id>', methods=['GET'])
def buscar_produto(id):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM produtos WHERE id = %s', (id,))
        produto = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not produto:
            return jsonify({"erro": "Produto não encontrado"}), 404
            
        return jsonify(produto), 200
        
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar produto: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

