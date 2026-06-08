# Sistema de Gestão de Stock Completo (CRUD)

Este é um projeto de backend desenvolvido em ambiente Termux, utilizando Python, Flask e PostgreSQL.

## 🛠️ Arquitetura da API (Porta 5001)

| Método | Endpoint | Descrição | Status |
| :--- | :--- | :--- | :--- |
| **GET** | `/produtos` | Lista todos os itens do stock | `200 OK` |
| **POST** | `/produtos` | Adiciona um novo produto | `201 Created` |
| **PUT** | `/produtos/<id>` | Atualiza dados de um item existente | `200 OK` |
| **DELETE** | `/produtos/<id>` | Remove permanentemente um item pelo ID | `200 OK` |

## 💻 Como Testar (Exemplos)

### Atualizar Produto (PUT)
curl -X PUT http://127.0.0.1:5001/produtos/1 -H "Content-Type: application/json" -d '{"nome": "Cobalt Bouazzer", "quantidade": 75, "preco": 1500.0}'

### Eliminar Produto (DELETE)
curl -X DELETE http://127.0.0.1:5001/produtos/1

