import datetime
import requests
from database import Database
from transacoes import Transacao
import graficos as gf
from tabulate import tabulate

class ControleFinanceiro:
    # Categorias definidas dentro da classe
    CATEGORIAS_RECEITA = ["Salário", "Freelance", "Outros"]
    CATEGORIAS_DESPESA = ["Alimentação", "Transporte", "Saúde", "Educação", "Lazer", "Moradia", "Outros"]
    FORMAS_PGTO = ["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "Pix", "Outros"]

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

    def saldo(self, lista=None):
        if lista is not None:
            transacoes = lista
        else:
            transacoes = self.transacoes

        soma_receita = 0
        soma_despesa = 0

        for tr in transacoes:
            if tr.tipo.lower() == "receita":
                soma_receita += tr.valor
            elif tr.tipo.lower() == "despesa":
                soma_despesa += tr.valor

        saldo = soma_receita - soma_despesa
        print(f"Saldo atual: R$ {saldo:.2f}")
        return saldo

    def listar_transacoes(self, lista=None):
        if lista is not None:
            transacoes = lista
        else:
            transacoes = self.transacoes

        print("\n=== Extrato de Transações ===")
        if not transacoes:
            print("Nenhuma transação registrada.")
            return

        # Prepara os dados para a tabela
        tabela_dados = []

        # Cabeçalho da tabela
        cabecalho = ["ID", "Data", "Tipo", "Categoria", "Valor (R$)", "Forma Pgto"]

        for i, t in enumerate(transacoes, start=1):
            # Formata a data para dia/mês/ano
            data_formatada = t.data.strftime("%d/%m/%Y")

            # Formata o tipo (Maiúsculo)
            tipo_formatado = t.tipo.upper()

            # Formata o valor (Alinhamento visual)
            valor_formatado = f"{t.valor:.2f}"

            # Adiciona a linha na lista da tabela
            tabela_dados.append([
                i,
                data_formatada,
                tipo_formatado,
                t.categoria,
                valor_formatado,
                t.forma_pgto
            ])

        # Imprime usando a biblioteca tabulate
        # tablefmt="fancy_grid" cria essas bordas bonitas conectadas
        print(tabulate(tabela_dados, headers=cabecalho, tablefmt="fancy_grid"))

    def exibir_menu_listagem(self):
        print("\n--- FILTRAR VISUALIZAÇÃO ---")
        print()
        print("[1] - Listar Receitas")
        print("[2] - Listar Despesas")
        print("[3] - Todas as Transações")
        print()

        try:
            op = int(input("Selecione: "))
        except ValueError:
            print("Opção inválida.")
            return

        lista_filtrada = []

        if op == 1:
            # Cria uma lista nova contendo apenas receitas
            lista_filtrada = [t for t in self.transacoes if t.tipo == 'receita']
            print(f"\n Exibindo apenas RECEITAS ({len(lista_filtrada)} registros):")

        elif op == 2:
            # Cria uma lista nova contendo apenas despesas
            lista_filtrada = [t for t in self.transacoes if t.tipo == 'despesa']
            print(f"\n Exibindo apenas DESPESAS ({len(lista_filtrada)} registros):")

        elif op == 3:
            # Usa a lista completa original
            lista_filtrada = self.transacoes
            print(f"\n Exibindo TODAS as transações ({len(lista_filtrada)} registros):")

        else:
            print("Opção inválida.")
            return

        # Chama o metodo que ja existe passando a lista acima
        self.listar_transacoes(lista_filtrada)


    def carregar_transacoes(self):
        self.transacoes = []  # limpa antes de carregar para evitar duplicação
        dados = self.db.buscar_transacoes()
        for d in dados:
            transacao = Transacao.from_dict(d)
            self.transacoes.append(transacao)

    def excluir_transacao(self):
        self.listar_transacoes()
        if not self.transacoes:
            return

        try:
            indice = int(input("Digite o número da transação a excluir: "))
            # a lista em Python começa em 0, mas mostrámos a partir de 1
            idx_real = indice - 1

            # verifica se o índice é positivo (>= 0) e se está dentro do limite da lista
            if idx_real >= 0 and idx_real < len(self.transacoes):
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



    def menu_relatorios(self):
        print("\n=== SELECIONE O PERÍODO ===")
        print()
        print("[1] - Últimos 30 dias")
        print("[2] - Últimos 60 dias")
        print("[3] - Últimos 90 dias")
        print("[4] - Último Ano (365 dias)")
        print("[5] - Todo o período")
        print("[0] - Voltar")

        try:
            op_periodo = int(input("Escolha o período: "))
        except ValueError:
            print("Opção inválida.")
            return

        if op_periodo == 0:
            return

        #filtragem de datas
        lista_filtrada = []
        if op_periodo == 5:
            lista_filtrada = self.transacoes
            print(f"\nSelecionado: Todo o período ({len(lista_filtrada)} transações)")
        else:
            dias_map = {1: 30, 2: 60, 3: 90, 4: 365}
            if op_periodo in dias_map:
                dias = dias_map[op_periodo]
                limite = datetime.date.today() - datetime.timedelta(days=dias)
                # Filtra apenas as que são mais recentes que o limite
                lista_filtrada = [t for t in self.transacoes if t.data >= limite]
                print(f"\nSelecionado: Últimos {dias} dias ({len(lista_filtrada)} transações)")
            else:
                print("Opção inválida.")
                return

        if not lista_filtrada:
            print("Não há dados neste período para gerar gráficos.")
            return

        #menu tipo de gráfico (loop para permitir ver vários sem sair)
        while True:
            print("\n--- TIPOS DE RELATÓRIO (GRÁFICO) ---")
            print()
            print("[1] - Gráfico: Receita x Despesa")
            print("[2] - Gráfico: Receitas por Categoria")
            print("[3] - Gráfico: Despesas por Categoria")
            print("[4] - Gráfico: Balanço do Período")
            print("[0] - Voltar ao menu principal")

            try:
                op_grafico = int(input("Escolha o gráfico: "))
            except ValueError:
                continue

            if op_grafico == 0:
                break

            elif op_grafico == 1:
                gf.plotar_receita_vs_despesa(lista_filtrada)
            elif op_grafico == 2:
                gf.plotar_categorias_receita(lista_filtrada)
            elif op_grafico == 3:
                gf.plotar_categorias_despesa(lista_filtrada)
            elif op_grafico == 4:
                gf.plotar_balanco_mensal(lista_filtrada)
            else:
                print("Opção inválida.")


    def escolher_categoria(self, tipo):
        if tipo == "receita":
            categorias = self.CATEGORIAS_RECEITA
        else:
            categorias = self.CATEGORIAS_DESPESA

        print(f"\nEscolha uma categoria de {tipo}:")
        for i, cat in enumerate(categorias, start=1):
            print(f"{i} - {cat}")
        try:
            op = int(input("Selecione: "))
            if 1 <= op <= len(categorias):
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

    def escolher_forma_pgto(self):
        print("\nEscolha a forma de pagamento ou recebimento: ")
        for i, f in enumerate(self.FORMAS_PGTO, start=1):
            print(f"{i} - {f}")
        try:
            op = int(input("Selecione: "))
            if 1 <= op <= len(self.FORMAS_PGTO):
                return self.FORMAS_PGTO[op - 1]
        except ValueError:
            pass
        print("Opção inválida. Forma de pagamento definida como 'Outros'.")
        return "Outros"