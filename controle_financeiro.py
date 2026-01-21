import datetime
from database import Database
from transacoes import Transacao
import requests

class ControleFinanceiro:
    # Categorias definidas dentro da classe
    CATEGORIAS_RECEITA = ["Salário", "Freelance", "Outros"]
    CATEGORIAS_DESPESA = ["Alimentação", "Transporte", "Saúde", "Educação", "Lazer", "Moradia", "Outros"]
    FORMAS_PGTO = ["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "Pix", "Outros"]      # nova lista

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


    def listar_transacoes(self, lista=None):
        if lista is not None:
            transacoes = lista
        else:
            transacoes = self.transacoes

        print("=== Lista de Transações ===")
        if not transacoes:
            print("Nenhuma transação registrada.")
        else:
            # O enumerate começa do 1
            for i, t in enumerate(transacoes, start=1):
                print(f"{i} - {t}")


    def excluir_transacao(self):
        self.listar_transacoes()
        if not self.transacoes:
            return

        try:
            indice = int(input("Digite o número da transação a excluir: "))

            #a lista em Python começa em 0, mas mostrámos a partir de 1
            idx_real = indice - 1

            #verifica se o índice é positivo (>= 0) e se está dentro do limite da lista
            if (idx_real >= 0 and idx_real < len(self.transacoes)):
                transacao_remover = self.transacoes[idx_real]

                # 1. Remove do Banco de Dados
                self.db.remover_transacao(transacao_remover)

                # 2. Remove da Lista em Memória
                self.transacoes.pop(idx_real)

                print("Transação removida com sucesso!")
            else:
                print("Número inválido.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


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



    def converter_dolar_para_real(self, valor_em_dolar):
        try:
            print("Consultando cotação do Dólar...")
            url = "https://economia.awesomeapi.com.br/last/USD-BRL"
            resposta = requests.get(url)

            if resposta.status_code == 200:
                dados = resposta.json()
                # 'bid' é o valor de compra (geralmente usado como referência de mercado)
                cotacao = float(dados['USDBRL']['bid'])
                valor_convertido = valor_em_dolar * cotacao

                print(f"Cotação Atual: R$ {cotacao:.2f}")
                print(f"Valor Convertido: US$ {valor_em_dolar:.2f} -> R$ {valor_convertido:.2f}")
                return valor_convertido
            else:
                print("Erro ao conectar na API. Usando valor original.")
                return valor_em_dolar
        except Exception as e:
            print(f"Erro na conversão: {e}")
            return valor_em_dolar

    def escolher_forma_pgto(self):                   # novo mét. escolher forma de pagamento
        print("\nEscolha a forma de pagamento ou recebimento: ")
        for i, f in enumerate(self.FORMAS_PGTO, start=1):
            print(f"{i} - {f}")
        try:
            op = int(input("Selecione: "))
            if (1 <= op <= len(self.FORMAS_PGTO)):
                return self.FORMAS_PGTO[op - 1]
        except ValueError:
            pass
        print("Opção inválida. Forma de pagamento definida como 'Outros'.")
        return "Outros"