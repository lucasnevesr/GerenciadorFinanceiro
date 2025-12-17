import datetime
from transacoes import Transacao
from controle_financeiro import ControleFinanceiro

def menu():              # criação da função menu
    obj_cf = ControleFinanceiro()   #Criação do objeto apartir da Classe ControleFinanceiro

    while True:
        print("\n----- |MENU| -----")
        print("1 - Nova Receita")
        print("2 - Nova Despesa")
        print("3 - Listar Transação")
        print("4 - Consultar Saldo")
        print("5 - Relatório")
        print("0 - Sair")

        try:
            op = int(input("Selecione a opção desejada: "))
        except ValueError:
            print("Entrada inválida! Digite um valor numérico.")
            continue

        if (op == 1):
            try:
                valor = float(input("Digite o valor da receita: "))
                if (valor < 0):
                    print("O valor não pode ser negativo.")
                    continue
            except ValueError:
                print("Entrada inválida.")
                continue
            data = datetime.date.today()
            categoria = input("Digite a categoria: ")
            transacao = Transacao("receita", valor, data, categoria)
            obj_cf.nova_receita(transacao)

        elif (op == 2):
            try:
                valor = float(input("Digite o valor da despesa: "))
                if (valor < 0):
                    print("O valor não pode ser negativo.")
                    continue
            except ValueError:
                print("Entrada inválida.")
                continue
            data = datetime.date.today()
            categoria = input("Digite a categoria: ")
            transacao = Transacao("despesa", valor, data, categoria)
            obj_cf.nova_despesa(transacao)

        elif (op == 3):
            obj_cf.listar_transacoes()

        elif (op == 4):
            obj_cf.saldo()

        elif (op == 5):
            obj_cf.relatorio_30dias()

        elif (op == 0):
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida, tente novamente.")

if __name__== "__main__":
    menu()

