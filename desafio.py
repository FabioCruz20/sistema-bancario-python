menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        deposito = float(input("Informe o valor do depósito: "))

        if deposito <= 0:
            print("Operação inválida: o valor do depósito deve ser maior que zero.")
        else:        
            saldo += deposito
            extrato += f"Depósito: R$ {deposito:.2f}\n"

    elif opcao == "s":
        if numero_saques >= LIMITE_SAQUES:
            print("Operação inválida: o número limite de saques foi excedido.")
            continue

        saque = float(input("Informe o valor do saque: "))

        if saque <= 0:
            print("Operação inválida: o valor do saque deve ser maior que zero.")
        elif saque > limite:
            print(f"Operação inválida: o valor do saque deve ser menor ou igual a {limite}.")
        elif saque > saldo:
            print("Operação inválida: saldo insuficiente para realizar o saque.")
        else:
            saldo -= saque
            extrato += f"Saque: R${saque:.2f}\n"
            numero_saques += 1

    elif opcao == "e":
        print("Extrato".center(50, "-"))
        if len(extrato) == 0:
            print("Não foram realizadas movimentações")
        else:
            print(extrato)
            print(f"Saldo: R$ {saldo:.2f}")
        print("-" * 50)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
