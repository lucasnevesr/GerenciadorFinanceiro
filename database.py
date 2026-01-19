from pymongo import MongoClient
import datetime
from dados_db import mongo_pass, mongo_user

class Database:
    def __init__(self):
        try:
            self.client = MongoClient(
                f"mongodb+srv://{mongo_user}:{mongo_pass}@cluster0.lhhjnfe.mongodb.net/?appName=Cluster0",
                serverSelectionTimeoutMS=5000
            )

            # 🔹 PING no MongoDB
            self.client.admin.command("ping")
            print("Conexão com MongoDB estabelecida com sucesso")

            self.db = self.client["controle_financeiro"]
            self.collection = self.db["transacoes"]

        except Exception as e:
            print("Erro ao conectar no MongoDB")
            print(e)
            raise  # força erro para não rodar app sem DB

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
