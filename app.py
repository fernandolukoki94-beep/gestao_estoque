from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def conectar_banco():
    conexao = sqlite3.connect('estoque.db')
    conexao.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
    return conexao

# 1. C - CREATE (Inserir um novo produto)
@app.route('/produtos', methods=['POST'])
def adicionar_produto():
    dados = request.get_json()
    nome = dados.get('nome')
    quantidade = dados.get('quantidade')
    preco = dados.get('preco')
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(
        'INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)',
        (nome, quantidade, preco)
    )
    conexao.commit()
    id_gerado = cursor.lastrowid
    conexao.close()
    
    return jsonify({"mensagem": "Produto adicionado!", "id": id_gerado}), 201

# 2. R - READ (Listar todos os produtos)
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM produtos')
    linhas = cursor.fetchall()
    conexao.close()
    
    # Converte os resultados do SQL para formato JSON
    produtos = [dict(linha) for line in [linhas] for linha in line] # Garante conversão limpa
    return jsonify(produtos), 200

# 3. U - UPDATE (Atualizar dados de um produto existente)
@app.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    dados = request.get_json()
    nome = dados.get('nome')
    quantidade = dados.get('quantidade')
    preco = dados.get('preco')
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(
        'UPDATE produtos SET nome = ?, quantidade = ?, preco = ? WHERE id = ?',
        (nome, quantidade, preco, id)
    )
    conexao.commit()
    linhas_afetadas = cursor.rowcount
    conexao.close()
    
    if linhas_afetadas == 0:
        return jsonify({"erro": "Produto não encontrado"}), 404
        
    return jsonify({"mensagem": "Produto atualizado com sucesso!"}), 200

# 4. D - DELETE (Remover um produto do estoque)
@app.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conexao.commit()
    linhas_afetadas = cursor.rowcount
    conexao.close()
    
    if linhas_afetadas == 0:
        return jsonify({"erro": "Produto não encontrado"}), 404
        
    return jsonify({"mensagem": "Produto removido com sucesso!"}), 200

if __name__ == '__main__':
    # Roda o servidor localmente na porta 5000
    app.run(debug=True, host='0.0.0.0', port=5000)

