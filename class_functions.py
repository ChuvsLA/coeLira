from datetime import datetime
import pytz
from flask import Flask

app = Flask(__name__)


class Banco:

    """
    Para registrar o banco do cliente e da conta destino.
    Realiza transações, analisa se o pagamento foi recusado, reembolsado ou recusado.
    Atributos:
    Titular: nome do titular da conta.
    Numero_conta: número da conta do titular.
    CPF: CPF do titular da conta.
    Agencia: número da agência do titular.
    Validade: número de validade impresso no cartão.
    Codigo_seguranca: código de segurança impresso no cartão.
    Conta: tipo de conta, ou seja, se é conta corrente ou poupança.
    Saldototal: toda vez que uma transação for feita o valor da transação vai somar à essa variável.
    Transacoes: toda vez que uma transação for feita, será incluída aqui.
    """

    @staticmethod
    def _data_hora():
        fuso_BR = pytz.timezone('Brazil/East')
        horario_BR = datetime.now(fuso_BR)
        return horario_BR.strftime('%d/%m/%Y %H:%M:%S')

    def __init__(self, titular, numero_conta, cpf, agencia, validade_cartao, codigo_seguranca, conta_corrente,
                 email_cliente):
        self._titular = titular
        self._numero_conta = numero_conta
        self._cpf = cpf
        self.agencia = agencia
        self._validade = validade_cartao
        self.__codigo_seguranca = codigo_seguranca
        self.conta = conta_corrente
        self._saldototal = 0
        self.email = email_cliente
        self.transacoes = []

    def consultar_saldototal(self):
        print('Seu saldo atual é de R${:,.2f}'.format(self._saldototal))

    def _depositar(self, valor):
        self._saldototal += valor
        self.transacoes.append((valor, self._saldototal, Banco._data_hora()))

    def _transferencia(self, valor, conta_destino):
        self._saldototal -= valor
        self.transacoes.append((-valor, self._saldototal, Banco._data_hora()))
        conta_destino._saldototal += valor
        conta_destino.append((-valor, conta_destino, Banco._data_hora()))

    def _pagamento_aprovado(self, valor, email):
        if self.transferencia() == valor:
            print(f'Liberar acesso e mandar mensagem de boas vindas no seguinte email: {email.cliente}.')
            return True

    def pagamento_recusado(self, valor):
        if self.transferencia() != valor:
            print('Seu pagamento foi recusado.')
            return True

    def reembolso(self, valor,  conta_destino):
        if conta_destino -= valor:
            self.transacoes.append((-valor,self._saldototal, Banco._data_hora))
            self._saldototal += valor
            self.transacoes.append((-valor, self._saldototal, Banco._data_hora()))
            return True
        else:
            print('Deu algo errado com o seu reembolso. Ligue na assistência técnica.')

    def historico_transacoes(self):
        print('Histórico de Transações:')
        print('Valor, Saldo, Data e Hora')
        for transacao in self.transacoes:
            print(transacao)


class TelaInformacoes:

    """
    Quando o usuário pesquisar os termos nome e email, retornará as informações do cliente em questão.
    Atributos:
    nome_item = Pesquise as tratativas com o nome do cliente.
    email_item = Pesquise as tratativas com o email do cliente.
    transacao = Ajuda a encontrar o histórico de todas as transações.
    """

    def __init__(self, nome_item, email_item, transacao):
        self.nome_item = nome_item
        self.email_item = email_item
        self.transacao = transacao.Banco.historico_transacoes()

    def acessar_nomestatus(self, df, nome_item, status):
        df= self.nome_item == df[df['nome']]
        df.reset_index(inplace = True)
        status = df['status']
        return status

    def acessar_emailstatus(self, df, email_item, status):
        df = self.email_item == df[df['email']]
        df.reset_index(inplace=True)
        status = df['status']
        return status

    def acessar_nomepagamento(self, df, nome_item, forma_pagamento):
        df = self.nome_item == df[df['nome']]
        df.reset_index(inplace=True)
        forma_pagamento = df['forma_pagamento']
        return forma_pagamento

    def acessar_emailpagamento(self, df, email_item, forma_pagamento):
        df = self.email_item == df[df['email']]
        df.reset_index(inplace=True)
        forma_pagamento = df['forma_pagamento']
        return forma_pagamento

    def acessar_nomeparcelas(self, df, nome_item, parcelamento):
        df = self.nome_item == df[df['nome']]
        df.reset_index(inplace=True)
        parcelamento = df['parcelas']
        return parcelamento

    def acessar_emailparcelas(self, df, email_item, parcelamento):
        df = self.email_item == df[df['email']]
        df.reset_index(inplace=True)
        parcelamento = df['parcelas']
        return parcelamento

    def acessar_historico(self, transacao, df):
        Banco.historico_transacoes()
        df = self.transacao == df[df['histórico']]
        df.reset_index(inplace=True)
        transacao = df['histórico']
        return transacao

    @app.route('/')
    def index(self, index_template, status):
        return index_template.format(message=status)

    index_statustemplate = """
        <div> O status do cliente é: {message} </div>
        """

    @app.route('/')
    def index(self, index_template, forma_pagamento):
        return index_template.format(message=forma_pagamento)

    index_pagamentotemplate = """
        <div> O tipo do pagamento do cliente foi: {message} </div>
        """

    @app.route('/')
    def index(self, index_template, parcelamento):
        return index_template.format(message=parcelamento)

    index_parcelastemplate = """
        <div> O cliente parcelou em: {message} </div>
        """