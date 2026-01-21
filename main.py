import datetime
from transacoes import Transacao
from controle_financeiro import ControleFinanceiro



def ler_data():
    while True:
        entrada = input("Informe a Data (dd/mm/aaaa) ou [Enter para hoje]: ")

        #se o usuário der enter (string vazia), retorna data de hoje
        if not entrada:
            return datetime.date.today()

        try:
            #tenta converter o texto para data
            data_formatada = datetime.datetime.strptime(entrada, "%d/%m/%Y").date()
            return data_formatada
        except ValueError:
            print("Formato inválido! Use dia/mês/ano (ex: 25/12/2025).")


# -------------------

def menu():
    obj_cf = ControleFinanceiro()

    while True:
        print("\n----- |MENU| -----")
        print("1 - Nova Receita")
        print("2 - Nova Despesa")
        print("3 - Listar Transação")
        print("4 - Consultar Saldo")
        print("5 - Relatório")
        print("6 - Remover Transação")
        print("0 - Sair")

        try:
            op = int(input("Selecione a opção desejada: "))
        except ValueError:
            print("Entrada inválida! Digite um valor numérico.")
            continue

        if op == 1 or op == 2:
            tipo_txt = "receita" if op == 1 else "despesa"

            try:
                valor_inicial = float(input(f"Digite o valor da {tipo_txt}: "))
                if valor_inicial < 0:
                    print("O valor não pode ser negativo.")
                    continue
            except ValueError:
                print("Entrada inválida.")
                continue

            #  LÓGICA DE MOEDA
            print("Moeda: [1] Real (BRL) - Padrão | [2] Dólar (USD)")
            opcao_moeda = input("Selecione: ")

            valor_final = valor_inicial

            if opcao_moeda == '2':
                valor_final = obj_cf.converter_dolar_para_real(valor_inicial)

            #DATA PERSONALIZADA
            data = ler_data()
            # --------------------------

            categoria = obj_cf.escolher_categoria(tipo_txt)

            #forma de pagamento
            forma_pgto = obj_cf.escolher_forma_pgto()

            transacao = Transacao(tipo_txt, valor_final, data, categoria, forma_pgto)

            if op == 1:
                obj_cf.nova_receita(transacao)
            else:
                obj_cf.nova_despesa(transacao)

        elif (op == 3):
            obj_cf.listar_transacoes()

        elif (op == 4):
            obj_cf.saldo()

        elif (op == 5):
            obj_cf.relatorio_30dias()

        elif (op == 6):
            obj_cf.excluir_transacao()

        elif (op == 0):
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    menu()