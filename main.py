import datetime
import os  #importar para controlar o terminal
from transacoes import Transacao
from controle_financeiro import ControleFinanceiro


#limpa a tela logo ao abrir o programa
def limpar_tela():
    #verifica se é windows ou linux/mac para usar o comando certo
    os.system('cls' if os.name == 'nt' else 'clear')


def pausa():
    print("\n")  #pula uma linha antes
    input("Pressione [ENTER] para continuar...")
    print("\n")
    limpar_tela()


# --- FUNÇÃO DE DATA ---
def ler_data():
    while True:
        print("\n")  # Pula linha para não grudar
        entrada = input("Informe a Data (dd/mm/aaaa) ou [Enter para hoje]: ")

        if not entrada:
            return datetime.date.today()

        try:
            data_formatada = datetime.datetime.strptime(entrada, "%d/%m/%Y").date()
            return data_formatada
        except ValueError:
            print("❌ Formato inválido! Use dia/mês/ano (ex: 25/12/2025).")


# -------------------

def menu():
    obj_cf = ControleFinanceiro()
    limpar_tela()

    while True:

        print("=" * 30)
        print("      SISTEMA FINANCEIRO      ")
        print("=" * 30)

        print("[1] - Nova Receita")
        print("[2] - Nova Despesa")
        print("[3] - Listar Transações")
        print("[4] - Consultar Saldo")
        print("[5] - Relatórios (Gráficos)")
        print("[6] - Remover Transação")
        print("[7] - Editar Transação")
        print("[0] - Sair")
        print("-" * 30)  #linha divisória

        try:
            op_txt = input("Selecione a opção desejada: ")
            print()
            # Se o usuário der enter sem digitar nada, evita erro
            if not op_txt:
                limpar_tela()
                continue
            op = int(op_txt)
        except ValueError:
            limpar_tela()
            print("\n❌ Entrada inválida! Digite um valor numérico.")
            continue

        if op == 1 or op == 2:
            tipo_txt = "Receita" if op == 1 else "Despesa"

            print(f"\n--- Nova {tipo_txt} ---")  # Cabeçalho da ação

            try:
                valor_inicial = float(input(f"Digite o valor da {tipo_txt}: R$ "))
                if valor_inicial < 0:
                    print("⚠️ O valor não pode ser negativo.")
                    pausa()
                    continue
            except ValueError:
                print("❌ Entrada inválida.")
                pausa()
                continue

            #  LÓGICA DE MOEDA
            print("\nMoeda da transação:")
            print("[1] Real (BRL) - Padrão")
            print("[2] Dólar (USD)")
            opcao_moeda = input("Selecione: ")

            valor_final = valor_inicial

            if opcao_moeda == '2':

                print("\n")
                valor_final = obj_cf.converter_dolar_para_real(valor_inicial)

            # DATA
            data = ler_data()

            # CATEGORIA
            categoria = obj_cf.escolher_categoria(tipo_txt.lower())

            # FORMA DE PAGAMENTO
            forma_pgto = obj_cf.escolher_forma_pgto()

            transacao = Transacao(tipo_txt.lower(), valor_final, data, categoria, forma_pgto)

            print("\n")  # Espaço antes de confirmar
            if op == 1:
                obj_cf.nova_receita(transacao)
            else:
                obj_cf.nova_despesa(transacao)

            # AQUI ESTÁ O SEGREDO: Pausa para ler, depois limpa
            pausa()

        elif (op == 3):
            limpar_tela()  # Limpa antes de mostrar a lista para focar nos dados
            obj_cf.exibir_menu_listagem()
            pausa()

        elif (op == 4):
            print("\n")
            obj_cf.saldo()
            pausa()

        elif (op == 5):
            limpar_tela()
            obj_cf.menu_relatorios()
            limpar_tela()  # Limpa ao voltar dos relatórios

        elif (op == 6):
            limpar_tela()
            obj_cf.excluir_transacao()
            pausa()

        elif (op == 7):
            limpar_tela()
            obj_cf.editar_transacao()
            pausa()

        elif (op == 0):
            print("\nSaindo do sistema... Até logo!")
            break

        else:
            print("\n⚠️ Opção inválida, tente novamente.")
            pausa()


if __name__ == "__main__":
    menu()