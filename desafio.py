import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

class Transacao(ABC):

    @property
    @abstractmethod
    def valor():
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):

    def __init__(self, valor = 0.0):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):

    def __init__(self, valor = 0.0):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Historico:

    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao: Transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })

    @property
    def transacoes(self):
        return self._transacoes


class Conta(ABC):


    def __init__(self, numero: int, cliente):
        self._agencia = "0001"
        self._numero = numero
        self._saldo = 0
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero: int):
        return cls(numero, cliente)
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def cliente(self):
        return self._cliente

    @property
    def agencia(self):
        return self._agencia
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("@@@ Operação falhou! Saldo insuficiente. @@@")
        if valor > 0:
            self._saldo -= valor
            print("=== Saque realizado com sucesso! ===")
            return True
        else:
            print("@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("=== Depósito realizado com sucesso! ===")
            return True
        
        print("@@@ Operação falhou! O valor informado é inválido. @@@")
        return False


class ContaCorrente(Conta):

    def __init__(
            self, 
            numero: int, 
            cliente, 
            limite=500,
            limite_saques=3):        
        super().__init__(numero, cliente)
        self._numero_saques = 0
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):

        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("@@@ Operação inválida! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("@@@ Operação inválida! Número máximo de saques excedido. @@@")
        else:
            return super().sacar(valor)
        
        return False

    def __str__(self):
        return textwrap.dedent(f"""\
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
        """)

class Cliente(ABC):

    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta: Conta, transacao):
        transacao.registrar(conta)


class PessoaFisica(Cliente):

    def __init__(self, cpf: str, nome: str, data_nascimento: str, endereco: str):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


def depositar(clientes):
    
    cliente, conta = buscar_cliente_e_conta(clientes)
    conta_valida = cliente and conta
    
    if not conta_valida:
        return
    
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    
    cliente, conta = buscar_cliente_e_conta(clientes)
    conta_valida = cliente and conta
    
    if not conta_valida:
        return  
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):

    cliente, conta = buscar_cliente_e_conta(clientes)
    conta_valida = cliente and conta
    
    if not conta_valida:
        return

    print("Extrato".center(50, "="))

    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = "Nenhuma transação foi realizada."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
    
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("=" * 50)
    

def criar_cliente(clientes):

    cpf = input("Informe o CPF (somente dígitos): ")
    cliente = buscar_cliente(cpf, clientes)    

    if cliente:
        print("@@@ Cliente já foi cadastrado! @@@")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, numero - bairro - cidade/sigla estado): ")
    cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
    clientes.append(cliente)

    print("=== Cliente criado com sucesso. ===")


def criar_conta(numero_conta, clientes, contas):

    cpf = input("Informe o CPF (somente dígitos): ")
    cliente = buscar_cliente(cpf, clientes)
    
    if cliente:
        print("=== Conta criada com sucesso! ===")
        conta = ContaCorrente.nova_conta(cliente, numero_conta)
        cliente.contas.append(conta)
        contas.append(conta)
        return conta
    
    print("@@@ Cliente não encontrado! @@@")
    

def listar_contas(contas):
    
    for conta in contas:
        print("\n", "-" * 50)
        print(conta)


def buscar_cliente_e_conta(clientes: list[Cliente]):

    cpf = input("Informe o CPF (somente dígitos): ")
    cliente = buscar_cliente(cpf, clientes)

    if not cliente:
        print("@@@ Cliente não encontrado! @@@")
        return None, None
    
    if not cliente.contas:
        print("@@@ O cliente não possui contas! @@@")
        return None, None

    print("Contas".center(20, "="))
    for conta in cliente.contas:
        print(f"Nº: {conta.numero}\tSaldo: {conta.saldo}")

    numero_conta = int(input("Informe o número da conta: "))
    conta = buscar_conta(numero_conta, cliente.contas)

    if not conta:
        print("@@@ Conta não encontrada! @@@")
        return None, None
    
    return cliente, conta


def buscar_cliente(cpf, clientes):
    cliente_buscado = None
    for usuario in clientes:
        if usuario.cpf == cpf:
            cliente_buscado = usuario
            break
        
    return cliente_buscado


def buscar_conta(numero_conta, contas):    
    conta_buscada = None
    for conta in contas:
        if conta.numero == numero_conta:
            conta_buscada = conta
    
    return conta_buscada


def menu():
    menu = """

    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nu]\tNovo Cliente
    [nc]\tNova Conta
    [lc]\tListar Contas
    [q]\tSair

    => """
    return input(textwrap.dedent(menu))


def main():

    clientes: list[Cliente] = []
    contas: list[ContaCorrente] = []

    while True:

        opcao = menu()

        if opcao == "d":            
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":            
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida. Por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
