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
            "categoria": transacao.categoria,
            "forma_pgto": transacao.forma_pgto  # incluído no doc
        }
        self.collection.insert_one(documento)


    def buscar_transacoes(self):
        return list(self.collection.find({}, {"_id": 0}))


    def remover_transacao(self, transacao):
        # Cria um filtro com os dados exatos da transação para encontrar no banco
        filtro = {
            "tipo": transacao.tipo,
            "valor": transacao.valor,
            "data": datetime.datetime.combine(transacao.data, datetime.time()),
            "categoria": transacao.categoria,
            "forma_pgto": transacao.forma_pgto  # incluído no filtro
        }
        # delete_one apaga apenas a primeira ocorrência encontrada
        self.collection.delete_one(filtro)