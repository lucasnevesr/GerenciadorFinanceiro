import matplotlib
matplotlib.use('TkAgg') #força o python a abrir uma janela nova para o gráfico

import matplotlib.pyplot as plt
import numpy as np



def formatar_rotulo_pizza(valores):
    def formatar(pct):
        #calcula o valor absoluto baseado na porcentagem
        total = sum(valores)
        val = pct * total / 100.0
        #retorna porcentagem na linha de cima e valor em reais na linha de baixo
        return '{p:.1f}%\n(R$ {v:.2f})'.format(p=pct, v=val)

    return formatar


def plotar_receita_vs_despesa(transacoes):
    total_receitas = sum(t.valor for t in transacoes if t.tipo == "receita")
    total_despesas = sum(t.valor for t in transacoes if t.tipo == "despesa")

    if total_receitas == 0 and total_despesas == 0:
        print("Sem dados para gerar gráfico.")
        return

    valores = [total_receitas, total_despesas]
    labels = ["Receitas", "Despesas"]
    cores = ['#4CAF50', '#F44336']  #verde e vermelho

    plt.figure(figsize=(8, 6))
    plt.pie(valores, labels=labels, autopct=formatar_rotulo_pizza(valores), colors=cores, startangle=90)
    plt.title("Receita vs Despesa")
    plt.tight_layout()
    plt.show()


def plotar_categorias_receita(transacoes):
    dados = {}
    for t in transacoes:
        if t.tipo == "receita":
            dados[t.categoria] = dados.get(t.categoria, 0) + t.valor

    if not dados:
        print("Nenhuma receita encontrada no período.")
        return

    valores = list(dados.values())
    labels = list(dados.keys())

    plt.figure(figsize=(8, 8))
    plt.pie(valores, labels=labels, autopct=formatar_rotulo_pizza(valores))
    plt.title("Distribuição de Receitas por Categoria")
    plt.tight_layout()
    plt.show()


def plotar_categorias_despesa(transacoes):
    dados = {}
    for t in transacoes:
        if t.tipo == "despesa":
            dados[t.categoria] = dados.get(t.categoria, 0) + t.valor

    if not dados:
        print("Nenhuma despesa encontrada no período.")
        return

    valores = list(dados.values())
    labels = list(dados.keys())

    plt.figure(figsize=(8, 8))
    plt.pie(valores, labels=labels, autopct=formatar_rotulo_pizza(valores))
    plt.title("Distribuição de Despesas por Categoria")
    plt.tight_layout()
    plt.show()


def plotar_balanco_mensal(transacoes):
    # Dicionário para agrupar por (Ano, Mês)
    dados_mensais = {}

    for t in transacoes:
        chave = (t.data.year, t.data.month)

        if chave not in dados_mensais:
            dados_mensais[chave] = {"receita": 0, "despesa": 0}

        if t.tipo == "receita":
            dados_mensais[chave]["receita"] += t.valor
        elif t.tipo == "despesa":
            dados_mensais[chave]["despesa"] += t.valor

    if not dados_mensais:
        print("Sem dados suficientes para gráfico mensal.")
        return

    #ordena as chaves cronologicamente
    chaves_ordenadas = sorted(dados_mensais.keys())

    labels = []
    receitas = []
    despesas = []
    saldos = []

    for ano, mes in chaves_ordenadas:
        label_mes = f"{mes:02d}/{ano}"
        labels.append(label_mes)

        r = dados_mensais[(ano, mes)]["receita"]
        d = dados_mensais[(ano, mes)]["despesa"]

        receitas.append(r)
        despesas.append(d)
        saldos.append(r - d)

    x = np.arange(len(labels))
    largura = 0.25

    plt.figure(figsize=(10, 6))
    plt.bar(x - largura, receitas, width=largura, label='Receitas', color='blue')
    plt.bar(x, despesas, width=largura, label='Despesas', color='orange')
    plt.bar(x + largura, saldos, width=largura, label='Saldo', color='green')

    plt.title("Balanço Mensal (Período Selecionado)")
    plt.xlabel("Mês/Ano")
    plt.ylabel("Valores (R$)")
    plt.xticks(x, labels)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.3)

    plt.tight_layout()
    plt.show()