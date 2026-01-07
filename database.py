from pymongo import MongoClient
import datetime

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://nevessricardoo_db_user:wxe93UB6N1rCnWmO@cluster0.lhhjnfe.mongodb.net/?appName=Cluster0")
        self.db = self.client["controle_financeiro"]
        self.collection = self.db["transacoes"]

    def salvar_transacao(self, transacao):
        documento = {
            "tipo": transacao.tipo,
            "valor": transacao.valor,
            "data": datetime.datetime.combine(transacao.data, datetime.time()),
            "categoria": transacao.categoria
        }
        self.collection.insert_one(documento)

    def buscar_transacoes(self):
        return list(self.collection.find({}, {"_id": 0}))
