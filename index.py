import os

# ==========================================================
# Sistema de controle de posto de combustível - Posto Rota 101
# ==========================================================
# O sistema registra abastecimentos, calcula descontos, emite
# comprovantes e faz fechamento do dia. Não há integração externa.
# ==========================================================


# -------------------------------
# CLASSES
# -------------------------------
class Combustivel:
    """Representa um tipo de combustível com seu preço."""
    def __init__(self, combustivel, preco):
        self.combustivel = combustivel
        self.preco = preco


class Relatorio:
    """Armazena todas as vendas e gera relatórios."""
    def __init__(self):
        self.vendas = []  # Lista que vai guardar cada venda

    def registrar_venda(self, tipo_combustivel, litros, preco_por_litro):
        """Registra uma nova venda na lista."""
        total = litros * preco_por_litro
        venda = {
            "tipo": tipo_combustivel,
            "litros": litros,
            "preco_por_litro": preco_por_litro,
            "total": total
        }
        self.vendas.append(venda)
        print(f"Venda registrada: {litros}L de {tipo_combustivel} - R${total:.2f}")

    def relatorio(self):
        """Exibe o relatório de todas as vendas registradas."""
        print("\n=== RELATÓRIO DE VENDAS ===")
        total_geral = 0
        for v in self.vendas:
            print(f"{v['litros']}L de {v['tipo']} - R${v['total']:.2f}")
            total_geral += v['total']
        print(f"Total arrecadado: R${total_geral:.2f}\n")


class Pagamentos:
    """Gerencia os tipos de pagamento aceitos."""
    def __init__(self):
        self.tipos = ["pix", "dinheiro", "cartao"]

global c1, c2, posto
# -------------------------------
# VALORES PADRÃO DOS COMBUSTÍVEIS
# -------------------------------
c1 = Combustivel("alcool", 4.13)
c2 = Combustivel("gasolina", 5.63)


# -------------------------------
# FUNÇÕES AUXILIARES
# -------------------------------
def limpar_tela():
    """Limpa o terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


# -------------------------------
# LOGIN E MENUS
# -------------------------------
def login():
    print("================= Login - Postos Rota 101 =====================\n")
    operacao = input("Qual a sua função dentro do Posto? (funcionario/gerente): ").lower()

    if operacao == "funcionario":
        menufuncionario()
    elif operacao == "gerente":
        menuGerente()
    else:
        print("Não existe essa função, tente novamente.")

    return operacao


def menufuncionario():
    print("================= Menu - Postos Rota 101 =====================\n")
    print("1. Abastecer Carro")
    print("2. Outra opção")
    print("3. Ver fechamento do dia")
    opc = int(input("Escolha: "))

    if opc == 1:
        AbasteceCarro()
    elif opc == 2:
        print("Função 2 ainda não implementada")
    elif opc == 3:
        print("Fechamento do dia...")
    else:
        print("Opção inválida!")


def menuGerente():
    print("================= Gerência - Postos Rota 101 =====================\n")
    print("1. Alterar Valores dos combustíveis")
    print("2. Ver fechamento do dia")
    print("0. Sair")
    opc = int(input("Escolha: "))

    if opc == 1:
        ValorCombustivel()
    elif opc == 2:
        fechamento()
        posto.relatorio()  # ⚠️ POSSÍVEL ERRO: 'posto' pode não existir ainda
    elif opc == 0:
        saida()
    else:
        print("Opção inválida!")


def saida():
    y = input("Deseja sair? (S/N): ").lower()
    return y


# -------------------------------
# ALTERAR VALORES DOS COMBUSTÍVEIS
# -------------------------------
def ValorCombustivel():
    """Permite ao gerente alterar o valor dos combustíveis."""
    global c1, c2
    combopc = input("Deseja alterar o valor do Alcool ou da Gasolina? ").lower()

    if combopc == "alcool":
        x = float(input("Novo valor do Alcool: "))
        c1 = Combustivel("alcool", x)
        print(f"Valor do álcool alterado para {c1.preco}")
    elif combopc == "gasolina":
        x = float(input("Novo valor da Gasolina: "))
        c2 = Combustivel("gasolina", x)
        print(f"Valor da gasolina alterado para {c2.preco}")
    else:
        print("Combustível inválido!")


# -------------------------------
# FUNÇÕES DE PAGAMENTO E DESCONTO
# -------------------------------
def pagamentoPix(forma, valorF):
    """Aplica desconto se for PIX ou dinheiro."""
    # ⚠️ ERRO LÓGICO AQUI:
    # a condição "if forma == 'pix' or 'dinheiro' or 1:" SEMPRE SERÁ VERDADEIRA
    # O certo seria:
    # if forma in ['pix', 'dinheiro']:
    if forma in ["pix" , "dinheiro" , 1]:
        valorF = valorF - (valorF * 0.02)
    return valorF


def descontarAlcool(litros, valor):
    """Aplica desconto no álcool dependendo da quantidade."""
    if litros > 50:
        desconto = 5
    else:
        desconto = 3
    valor_final = valor - (valor * (desconto / 100))
    return valor_final, desconto


def descontarGasosa(litros, valor):
    """Aplica desconto na gasolina dependendo da quantidade."""
    if litros > 50:
        desconto = 4
    else:
        desconto = 2
    valor_final = valor - (valor * (desconto / 100))
    return valor_final, desconto


# -------------------------------
# FUNÇÕES PRINCIPAIS
# -------------------------------
def Comprovante(formaPago, desconto, valorF, tipo_combustivel, litros):
    """Imprime o comprovante de compra."""
    limpar_tela()
    print("================= Comprovante de Compra =====================\n")
    print("Local: Posto Rota 101\n")
    print(f"Combustível: {tipo_combustivel}")
    print(f"Litros: {litros}")
    print(f"Forma de pagamento: {formaPago}")
    print(f"Desconto aplicado: {desconto}%")
    print(f"Valor final: R$ {valorF:.2f}")
    print("=============================================================\n")


def AbasteceCarro():
    """Executa o processo de abastecimento e registra a venda."""
   

    # ⚠️ ERRO GRAVE AQUI:
    # Toda vez que o funcionário abastece, você cria um NOVO Relatorio()
    # Isso apaga as vendas anteriores. O certo seria criar ele fora do loop principal.
    

    print("=============================================\n")
    opc_combustivel = int(input("Tipo de combustível usado será?\n1. Alcool\n2. Gasolina\n> "))
    litros = float(input("Quantos litros serão colocados? "))

    if opc_combustivel == 1:
        valor_inicial = c1.preco * litros
        valorF, desconto = descontarAlcool(litros, valor_inicial)
        tipo = c1.combustivel
    elif opc_combustivel == 2:
        valor_inicial = c2.preco * litros
        valorF, desconto = descontarGasosa(litros, valor_inicial)
        tipo = c2.combustivel
    else:
        print("Opção inválida!")
        return

    print(f"O valor a pagar será de R$ {valorF:.2f}")
    forma = input("Forma de pagamento (pix/dinheiro/cartao): ").lower()
    valorF = pagamentoPix(forma, valorF)
    print(f"Novo valor após desconto: R${valorF:.2f}")

    # ⚠️ ERRO: Faltam argumentos em registrar_venda()
    # O método espera (tipo_combustivel, litros, preco_por_litro)
    # Aqui está sendo chamado sem parâmetros.
    posto.registrar_venda(c1.tipo_combustivel, litros, c1.preco)

    comprovante = input("Deseja comprovante de compra? (s/n): ").lower()
    if comprovante in ["s", "sim"]:
        Comprovante(forma, desconto, valorF, tipo, litros)


def fechamento():
    """Mostra o fechamento do dia."""

    print("======================= Fechamento do Dia ===================\n")


# -------------------------------
# PROGRAMA PRINCIPAL
# -------------------------------
def main():
    while True:
        login()
        sair = saida()
        if sair == "s":
            break


if __name__ == "__main__":
    main()
