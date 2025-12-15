

class Transacao:
    def __init__(self, tipo, valor, data, categoria):
        self.tipo = tipo
        self.valor = valor
        self.data = data
        self.categoria = categoria


class ControleFinanceiro:
    def __init__(self):
        self.transacoes = []

    def novaReceita(self, t):
        self.transacoes.append(t)
        print(self.transacoes[0].tipo)

    def novaDespesa(self, valor, categoria, data):
        self.transacoes.append(Transacao("despesa", valor, data, categoria))

    def saldo(self):
        somaReceita = 0
        print("Cheguei aqui")
        print(self.transacoes[0].tipo)
        for t in self.transacoes:
            print("----")
            print(t.tipo)
            if t.tipo == "receita":
                somaReceita += t.valor

        somaDespesas = 0
        for t in self.transacoes:
            if t.tipo == "despesa":
                somaDespesas += t.valor

        print(somaReceita)
        print(somaDespesas)
        return somaReceita - somaDespesas

