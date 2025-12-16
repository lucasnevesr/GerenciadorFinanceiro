import datetime
from Transacao import ControleFinanceiro
from Transacao import Transacao


x = ControleFinanceiro()
p = 2
while True:

    print()
    print("MENU:")
    print()
    print("1 - nova receita")
    print("2 - nova despesa")
    print("3 - consultar saldo")
    print()
    opcao = int(input("Selecione uma das opções acima:"))
    print()


    if opcao == 1:
        valor = float(input("Digite o valor:"))
        data = datetime.date.today()
        categoria = str(input("Digite a categoria:"))
        transacao = Transacao("receita", valor, categoria, data)
        x.novaReceita(transacao)
        print(x.transacoes)

    elif opcao == 2:
        valor = float(input("Digite o valor:"))
        data = datetime.date.today()
        categoria = str(input("Digite a categoria:"))
        # x = ControleFinanceiro()
        # x.novaDespesa(valor, data, categoria)

    elif opcao == 3:
        x.saldo()