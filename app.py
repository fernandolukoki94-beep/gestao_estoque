from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)

def conectar_banco():
    # Obtém o utilizador atual do sistema automaticamente
    usuario_atual = os.getlogin()

    # Conecta ao PostgreSQL usando RealDictCursor
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="estoque_db",
        user=usuario_atual,
        port="5432",
        cursor_factory=RealDictCursor
    )
    return conn

# ==========================================
# 1. ROTA POST: ADICIONAR PRODUTO
# ==========================================
@app.route('/produtos', methods=['POST'])
def adicionar_produto():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400
        
    nome = dados.get('nome')
    quantidade = dados.get('quantidade')
    preco = dados.get('preco')
    
    if not nome or quantidade is None or preco is None:
        return jsonify({"erro": "Campos obrigatórios em falta"}), 400

    conn = conectar_banco()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO produtos (nome, quantidade, preco) VALUES (%s, %s, %s) RETURNING id;",
                (nome.strip(), quantidade, preco)
            )
            produto_id = cursor.fetchone()['id']
            conn.commit()
            return jsonify({"id": produto_id, "mensagem": "Produto adicionado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"erro": f"Erro na base de dados: {e}"}), 500
    finally:
        conn.close()

# ==========================================
# 2. ROTA GET: LISTAR TODOS OS PRODUTOS
# ==========================================
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    conn = conectar_banco()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM produtos ORDER BY id;")
            produtos = cursor.fetchall()
            return jsonify(produtos), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar: {e}"}), 500
    finally:
        conn.close()

# ==========================================
# 3. ROTA PUT: ATUALIZAR PRODUTO (A que estava a faltar!)
# ==========================================
@app.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Payload JSON ausente"}), 400
        
    nome = dados.get('nome')
    quantidade = dados.get('quantidade')
    preco = dados.get('preco')
    
    if not nome or quantidade is None or preco is None:
        return jsonify({"erro": "Campos obrigatórios em falta"}), 400

    conn = conectar_banco()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE produtos 
                SET nome = %s, quantidade = %s, preco = %s 
                WHERE id = %s;
                """,
                (nome.strip(), quantidade, preco, id)
            )
            conn.commit()
            if cursor.rowcount > 0:
                return jsonify({"mensagem": "Produto atualizado com sucesso!"}), 200
            return jsonify({"erro": "Produto não encontrado para atualização"}), 404
    except Exception as e:
        return jsonify({"erro": f"Erro ao atualizar: {e}"}), 500
    finally:
        conn.close()

# ==========================================
# 4. ROTA DELETE: ELIMINAR PRODUTO
# ==========================================
@app.route('/produtos/<int:id>', methods=['DELETE'])
def eliminar_produto(id):
    conn = conectar_banco()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM produtos WHERE id = %s;", (id,))
            conn.commit()
            if cursor.rowcount > 0:
                return jsonify({"mensagem": "Produto eliminado com sucesso!"}), 200
            return jsonify({"erro": "Produto não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": f"Erro ao eliminar: {e}"}), 
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)

