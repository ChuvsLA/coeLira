from flask import Flask, render_template, request, redirect
from TelaInformacoes import *
from Banco import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/webhook', methods= ['POST'])
def webhook(pagamento_aprovado, pagamento_recusado, reembolso):
    if request.method == 'POST':
        print(request.json)
        return 'Novo Webhook!'

    if pagamento_aprovado == True:
        Flask('Seu pagamento foi aprovado! Bem Vindo ao curso!')
        return redirect(url_for('index'))

    if pagamento_recusado == True:
        Flask('Seu pagamento foi recusado.')
        return redirect(url_for('index'))

    elif reembolso == True:
        Flask('Reembolso realizado. Acesso ao curso retirado.')
        return redirect(url_for('index'))

    @app.route('/')
    def index(self, index_template, acessar_historico):
        return index_template.format(message=acessar_historico)

    index_historicotemplate = """
            <div> Histórico: {message} </div>
            """

    @app.route('/')
    def index(self, index_template, consultar_saldototal):
        return index_template.format(message=consultar_saldototal)

    index_saldottemplate = """
            <div> Saldo Total: {message} </div>
            """

if __name__ == "__main__":
   app.run(debug = True)
app.run([host == '0.0.0.0', port == 8000])