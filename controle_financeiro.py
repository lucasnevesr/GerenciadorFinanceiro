import datetime
from database import Database
from transacoes import Transacao
import matplotlib
import requests

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
        import datetime
        import matplotlib.pyplot as plt
        import numpy as np

        hoje = datetime.date.today()
        limite = hoje - datetime.timedelta(days=30)
        transacoes_periodo = []

        # Filtrar transações
        for t in self.transacoes:
            if t.data >= limite:
                transacoes_periodo.append(t)

        print("\n=== Relatório dos últimos 30 dias ===")
        if not transacoes_periodo:
            print("Nenhuma transação registrada nesse período.")
            return

        # Seu relatório original
        self.listar_transacoes(transacoes_periodo)
        self.saldo(transacoes_periodo)

        def relatorio_30dias(self):
            import datetime
            import matplotlib.pyplot as plt

            hoje = datetime.date.today()
            limite = hoje - datetime.timedelta(days=30)
            transacoes_periodo = []

            # Filtrar transações
            for t in self.transacoes:
                if t.data >= limite:
                    transacoes_periodo.append(t)

            print("\n=== Relatório dos últimos 30 dias ===")
            if not transacoes_periodo:
                print("Nenhuma transação registrada nesse período.")
                return

            # Relatórios textuais
            self.listar_transacoes(transacoes_periodo)
            self.saldo(transacoes_periodo)

            # -----------------------------
            # 🟦 GRÁFICO PRINCIPAL: RECEITA x DESPESA x SALDO
            # -----------------------------
            total_receitas = sum(t.valor for t in transacoes_periodo if t.tipo == "receita")
            total_despesas = sum(t.valor for t in transacoes_periodo if t.tipo == "despesa")
            total_saldo = total_receitas - total_despesas

            valores = [total_receitas, total_despesas, total_saldo]
            labels = ["Receitas", "Despesas", "Saldo"]

            plt.figure(figsize=(7, 7))
            plt.pie(valores, labels=labels, autopct='%1.1f%%')
            plt.title("Receita x Despesa x Saldo — Últimos 30 dias")
            plt.tight_layout()
            plt.show()

            # -----------------------------
            # 🟩 GRÁFICO DE RECEITAS POR CATEGORIA
            # -----------------------------
            receitas_por_categoria = {cat: 0 for cat in CATEGORIAS_RECEITA}

            for t in transacoes_periodo:
                if t.tipo == "receita":
                    if t.categoria in receitas_por_categoria:
                        receitas_por_categoria[t.categoria] += t.valor
                    else:
                        receitas_por_categoria["Outros"] += t.valor

            valores_receita = list(receitas_por_categoria.values())
            labels_receita = list(receitas_por_categoria.keys())

            if sum(valores_receita) > 0:
                plt.figure(figsize=(7, 7))
                plt.pie(valores_receita, labels=labels_receita, autopct='%1.1f%%')
                plt.title("Receitas por Categoria — Últimos 30 dias")
                plt.tight_layout()
                plt.show()
            else:
                print("\nNenhuma receita registrada no período para gerar gráfico por categoria.")


        # -----------------------------
        # 🟦 GRÁFICO MENSAL DO PERÍODO
        # -----------------------------

        # Cria listas para meses e valores
        meses_ordem = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul",
                       "Ago", "Set", "Out", "Nov", "Dez"]

        receitas_mensais = {m: 0 for m in meses_ordem}
        despesas_mensais = {m: 0 for m in meses_ordem}

        # Popular dados APENAS do período
        for t in transacoes_periodo:
            mes_nome = meses_ordem[t.data.month - 1]

            if t.tipo == "receita":
                receitas_mensais[mes_nome] += t.valor
            elif t.tipo == "despesa":
                despesas_mensais[mes_nome] += t.valor

        # Listas para o gráfico
        meses = list(receitas_mensais.keys())
        receitas = list(receitas_mensais.values())
        despesas = list(despesas_mensais.values())
        saldo = [r - d for r, d in zip(receitas, despesas)]

        # Montar o gráfico
        x = np.arange(len(meses))
        largura = 0.25

        plt.figure(figsize=(10, 5))
        plt.bar(x - largura, receitas, width=largura, label='Receitas', color='blue')
        plt.bar(x, despesas, width=largura, label='Despesas', color='orange')
        plt.bar(x + largura, saldo, width=largura, label='Saldo', color='green')

        plt.title("Receita x Despesa x Saldo — Últimos 30 dias (por mês)")
        plt.xlabel("Meses")
        plt.ylabel("Valores (R$)")
        plt.xticks(x, meses)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.3)

        plt.tight_layout()
        plt.show()



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
