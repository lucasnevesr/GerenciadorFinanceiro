import datetime
from transacoes import Transacao

class ControleFinanceiro:
    def __init__(self):
        self.transacoes = [] # lista de objetos Transacao

    def nova_receita(self, obj_receita):
        self.transacoes.append(obj_receita)
        print("Receita adicionada:", obj_receita)


    def nova_despesa(self, obj_despesa):
        self.transacoes.append(obj_despesa)
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

