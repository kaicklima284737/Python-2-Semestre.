from pymongo import MongoClient
from pymongo import UpdateOne
from bson.decimal128 import Decimal128
import random
from nomes import novos_nomes
from profissoes import novas_profissoes
from controller import lista_usuarios

client = MongoClient("mongodb://localhost:27017/")

db = client["meu_banco"]

collection = db["usuarios"]

resultado = collection.insert_many(lista_usuarios)
print("\nID inserido:", resultado.inserted_ids) #Adicionar novos usuarios

""" 
--------------------------------------------------------------
Comando para atualizar todos os valores de saldo para 0.00
db.usuarios.update_many(
    {},
    {"$set": {"saldo R$": Decimal128("0.00")}}
)
--------------------------------------------------------------
todos acima de 20 anos
documento = collection.find({"idade": {"$gt": 20}})
for doc in documento:
    print(doc)
--------------------------------------------------------------
atualizar o 1 item de um documento
resultado = collection.update_one(
{"nome": "Leticia Carvalho"}, # Filtro
{"$set": {"idade": 31}} # Atualização
)
print("Número de documentos modificados:", resultado.modified_count)
--------------------------------------------------------------

# Atualizar múltiplos documentos
resultado = collection.update_many(
{"idade": {"$lt": 30}}, # Filtro / todos abaixo de 30 anos
{"$set": {"status": "jovem"}} # Atualização / criação de um status Jovem para abaixo de 30 anos
)
print("Número de documentos modificados:", resultado.modified_count)

{"idade": {"$lt": 60} and {"$gt": 30}}, # Filtro / todos abaixo de 60 anos e acima de 30, atribui status de
{"$set": {"status": "Adulto médio"}} #Adulto médio

{"idade": {"$gt": 60}}, # Filtro / todos acima de 60 anos.
{"$set": {"status": "Senhor(a)"}} # Atualização / criação de um status Senhor(a)
--------------------------------------------------------------
# Remover um único documento
resultado = colecao.delete_one({"nome": "José Roberto"})
print("Número de documentos deletados:", resultado.deleted_count)
--------------------------------------------------------------
# Remover múltiplos documentos
resultado = colecao.delete_many({"idade": {"$lt": 30}})
print("Número de documentos deletados:", resultado.deleted_count)
--------------------------------------------------------------
operacoes = [
    UpdateOne(
        {"_id": doc["_id"]},
        {"$set": {"saldo R$": f" {random.randint(-5000, 200000)}"}}
    )
    for doc in collection.find({}, {"_id": 1})
]

# Executa as alterações de uma só vez
if operacoes:
    collection.bulk_write(operacoes)
"""
