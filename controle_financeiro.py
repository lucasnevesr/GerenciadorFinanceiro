import datetime
from database import Database
from transacoes import Transacao

class ControleFinanceiro:
    # Categorias definidas dentro da classe
    CATEGORIAS_RECEITA = ["Salário", "Freelance", "Outros"]
    CATEGORIAS_DESPESA = ["Alimentação", "Transporte", "Saúde", "Educação", "Lazer", "Moradia", "Outros"]

    def __init__(self):
        self.transacoes = [] # lista de objetos Transacao
        self.db = Database()
        self.carregar_transacoes()

    def nova_receita(self, obj_receita):
        self.transacoes.append(obj_receita)
        self.db.salvar_transacao(obj_receita)
        print("Receita adicionada:", obj_receita)


    def nova_despesa(self, obj_despesa):
        self.transacoes.append(obj_despesa)
        self.db.salvar_transacao(obj_despesa)
        print("Despesa adicionada:", obj_despesa)

    def saldo(self, lista = None):
        if lista is not None:
            transacoes = lista
        else:
            transacoes = self.transacoes

        soma_receita = 0
        soma_despesa = 0

        for tr in transacoes:
            if (tr.tipo.lower() == "receita"):
                soma_receita += tr.valor

            elif (tr.tipo.lower() == "despesa"):
                soma_despesa += tr.valor

        saldo = soma_receita - soma_despesa
        print(f"Saldo atual: R$ {saldo:.2f}")

        return saldo


    def listar_transacoes(self, lista = None):

        if lista is not None:
            transacoes = lista
        else:
            transacoes = self.transacoes

        print("=== Lista de Transações ===")
        if not transacoes:
            print("Nenhuma transação registrada.")
        else:
            for t in transacoes:
                print(t)


    def relatorio_30dias(self):
        hoje = datetime.date.today()
        limite = hoje - datetime.timedelta(days=30)
        transacoes_periodo = []

        for t in self.transacoes:
            if (t.data >= limite):
                transacoes_periodo.append(t)

        print("\n=== Relatório dos últimos 30 dias ===")
        if not transacoes_periodo:
            print("Nenhuma transação registrada nesse período.")
            return

        self.listar_transacoes(transacoes_periodo)
        self.saldo(transacoes_periodo)


    def carregar_transacoes(self):
        self.transacoes = []  # limpa antes de carregar para evitar duplicação
        dados = self.db.buscar_transacoes()
        for d in dados:
            transacao = Transacao.from_dict(d)
            self.transacoes.append(transacao)

    def escolher_categoria(self, tipo):
        if (tipo == "receita"):
            categorias = self.CATEGORIAS_RECEITA
        else:
            categorias = self.CATEGORIAS_DESPESA

        print(f"\nEscolha uma categoria de {tipo}:")
        for i, cat in enumerate(categorias, start=1):
            print(f"{i} - {cat}")
        try:
            op = int(input("Selecione: "))
            if (1 <= op <= len(categorias)):
                return categorias[op - 1]
        except ValueError:
            pass
        print("Opção inválida. Categoria definida como 'Outros'.")
        return "Outros"
