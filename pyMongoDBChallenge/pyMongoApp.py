"""
I am implementing a MongoDB integration application based on a non-relational schema provided by the course teacher's
challenge.

Programmed by: Kaíque Freire
"""

from pprint import pprint

from bson import ObjectId
from pymongo.mongo_client import MongoClient

# Caminho do meu cluster
uri = "mongodb+srv://kaiquefreiresantos05:kaique2005@cluster0.0kml1yf.mongodb.net/?retryWrites=true&w=majority"

# Criando um cliente e conectando com o servidor
client = MongoClient(uri)

# Fazendo um teste para saber se estou conectado
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

except Exception as e:
    print(e)

# Criando o banco de dados
db = client.test

account_kaique = {
    "id": "01",
    "nome": "Kaique Freire",
    "cpf": "784236589",
    "account": [
        {
            "id": "01",
            "tipo": "corrente",
            "agencia": "1234",
            "num": 5678,
            "balance": 0,
        },
        {
            "id": "01",
            "tipo": "poupança",
            "agencia": "5678",
            "num": 9876,
            "balance": 5000.0,
        },
    ]
}

# Criando a tabela de string chamada accounts
accounts = db.accounts

"""
# Adicionando uma única string
accounts.insert_one(account_kaique)
"""

new_accounts = [{
    "id": "02",
    "name": "Maria Teresa",
    "cpf": "317983289",
    "account": [
        {
            "id": "02",
            "tipo": "corrente",
            "agencia": "1469",
            "num": 7891,
            "balance": 0,
        },
        {
            "id": "02",
            "tipo": "poupança",
            "agencia": "0675",
            "num": 7895,
            "balance": 200.50,
        }
    ]  # Terminando de adicionar os 2 tipos de contas

}, {
    "id": "03",
    "name": "Victor Peixoto",
    "cpf": "784269854",
    "account": [
        {
            "id": "03",
            "tipo": "corrente",
            "agencia": "9687",
            "num": 3247,
            "balance": 200.0,
        },
        {
            "id": "03",
            "tipo": "poupança",
            "agencia": "1465",
            "num": 4562,
            "balance": 10000.00,
        }
    ]
}]

"""
# Inserindo todos os string da variável
result = accounts.insert_many(new_accounts)
print(result.inserted_ids)
"""


"""
# O ObjectId do documento que queremos excluir
document_id = ObjectId('658f558e41df387cf1e216a3')

# Exclui o documento
accounts.delete_one({"_id": document_id})
"""

collections = db.list_collection_names()  # Pegando apenas os nomes das collections existentes

print("\nColeções presentes no cluster")
for collection in collections:
    print(collection)

print("\nDocumentos presentes na coleção accounts")
for account in accounts.find():  # Recuperando todos as info
    pprint(account)
    print()

client.drop_database('test')  # Deletando o banco de dados 'test'
print(db.list_collection_names())
