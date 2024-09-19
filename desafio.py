import textwrap

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):

    if valor <= 0:
        print("Operação inválida: o valor do saque deve ser maior que zero.")
    elif numero_saques == limite_saques:
        print(f"Operação inválida: o limite diário de {limite_saques} saques foi atingido.")
    elif valor > limite:
        print(f"Operação inválida: o valor do saque deve ser menor ou igual a {limite}.")
    elif valor > saldo:
        print("Operação inválida: saldo insuficiente para realizar o saque.")
    else:
        saldo -= valor
        extrato += f"Saque:\t\tR${valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso.")
    
    return saldo, extrato, numero_saques


def depositar(saldo, valor, extrato, /):

    if valor <= 0:
        print("Operação inválida: o valor do depósito deve ser maior que zero.")
    else:        
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("Depósito realizado com sucesso.")
    
    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):

    print("Extrato".center(50, "-"))
    if len(extrato) == 0:
        print("Não foram realizadas movimentações")
    else:
        print(extrato)
        print(f"Saldo:\t\tR$ {saldo:.2f}")
    print("-" * 50)


def criar_usuario(usuarios):

    cpf = input("Informe o CPF (somente dígitos): ")
    usuario = buscar_usuario(cpf, usuarios)    

    if usuario:
        print("Operação inválida: usuário já foi cadastrado.")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, numero - bairro - cidade/sigla estado): ")
    usuario = {
        "nome": nome, 
        "data_nascimento": data_nascimento, 
        "cpf": cpf, 
        "endereco": endereco
    }
    usuarios.append(usuario)

    print("Usuário criado com sucesso.")


def criar_conta(agencia, numero, usuarios):

    cpf = input("Informe o CPF (somente dígitos): ")

    usuario = buscar_usuario(cpf, usuarios)
    
    if usuario:
        print("Conta criada com sucesso.")

        return {
            "agencia": agencia,
            "numero": numero,
            "usuario": usuario,
        }
    
    print("Operação inválida: CPF não encontrado.")
    

def listar_contas(contas):
    
    for conta in contas:

        agencia = conta['agencia']
        numero = conta['numero']
        nome = conta['usuario']['nome']

        print("\n", "-" * 50)
        print(f"Agência:\t{agencia}")
        print(f"Número:\t\t{numero}")
        print(f"Nome:\t\t{nome}")


def buscar_usuario(cpf, usuarios):

    usuario_buscado = None
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            usuario_buscado = usuario
            break
    
    return usuario_buscado


def menu():
    menu = """

    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nu]\tNovo Usuário
    [nc]\tNova Conta
    [lc]\tListar Contas
    [q]\tSair

    => """
    return input(textwrap.dedent(menu))


def main():

    saldo = 0
    extrato = ""
    numero_saques = 0
    LIMITE_VALOR_SAQUE = 500
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    numero_conta = 1
    usuarios = []
    contas = []

    while True:

        opcao = menu()

        if opcao == "d":
            deposito = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, deposito, extrato)

        elif opcao == "s":
            saque = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo, 
                valor=saque, 
                extrato=extrato,                                               
                limite=LIMITE_VALOR_SAQUE, 
                numero_saques=numero_saques, 
                limite_saques=LIMITE_SAQUES)

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)
            
        elif opcao == "nc":
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
                numero_conta += 1

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida. Por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
