# saved as greeting-client.py
import Pyro5.api
import getopt
import sys
import time

import werkzeug
from flask import Flask, request, redirect, render_template




app = Flask(__name__)
# aeroporto
aeroporto = {}
dados_aero = {}

# hotel

hotel = {}
dados_hotel = {}

passeio = {}
dados_passeio = {}


nameserver=Pyro5.core.locate_ns(port=5050)
uriHosp=nameserver.lookup("hospServer.tp2")
uriTicket=nameserver.lookup("ticketServer.tp2")
uriPass=nameserver.lookup("passeioServer.tp2")



@app.route('/', methods=['POST', 'GET'])  # home.html
def index():
    ticketClass = Pyro5.api.Proxy(uriTicket)
    if request.method == 'POST':
        aero = request.form['aeroporto']
        data_ida = request.form['dataida']
        data_volta = request.form['datavolta']
        passagens = request.form['npassagens']

        data = {
            "paraAeroporto": aero,
            "dataIda": data_ida,
            "dataVolta": data_volta,
            "numeroPassagens": passagens
        }

        start = time.time()
        aeroporto = ticketClass.getTickets({'action': 'passagem', **data})
        #print(aeroporto)
        end = time.time()
        print(f"Tempo Server Aero: {end - start}s")
        dados_aero['aero_ida'] = aeroporto['ida']
        dados_aero['aero_volta'] = aeroporto['volta']

        return redirect('/aero')

    return render_template('index.html')


@app.route('/aero', methods=['POST', 'GET'])
def showAero():
    if request.method == 'POST':
        return redirect('/hotel')
    return render_template('showAero.html', aero_ida=dados_aero['aero_ida'], aero_volta=dados_aero['aero_volta'])


@app.route('/hotel', methods=['POST', 'GET'])
def selectHotel():
    hospClass = Pyro5.api.Proxy(uriHosp)
    if request.method == 'POST':
        cidades = request.form['cidades']
        dataidahotel = request.form['dataidahotel']
        datavoltahotel = request.form['datavoltahotel']
        npessoas = request.form['npessoas']

        data = {
            "cidade": cidades,
            "numeroDePessoas": npessoas,
            "dataIda": dataidahotel,
            "dataVolta": datavoltahotel,
        }

        start = time.time()
        hotel = hospClass.getHosps({'action': 'hospedar', **data})
        end = time.time()
        print(f"Tempo Server Hotel: {end - start}s")

        dados_hotel['hosp'] = hotel['hospedagens']

        return redirect('/showHotel')
    return render_template('hotel.html')


@app.route('/showHotel', methods=['POST', 'GET'])
def showHoteis():
    if request.method == 'POST':
        return redirect('/passeio')
    return render_template('showHotel.html', hosp=dados_hotel['hosp'])


@app.route('/passeio', methods=['POST', 'GET'])
def selectPasseio():
    passeioClass = Pyro5.api.Proxy(uriPass)
    if request.method == 'POST':
        print(request.form)
        cidadePasseio = request.form['cidade']
        dataidaPasseio = request.form['dataidaPasseio']

        data = {
            "cidade": cidadePasseio,
            "dataIda": dataidaPasseio
        }

        start = time.time()
        passeio = passeioClass.getPasseios({**data})
        end = time.time()
        print(f"Tempo Server Passeio: {end - start}s")

        dados_passeio['passeio'] = passeio['passeio']

        return redirect('/showPasseio')
    return render_template('passeio.html')


@app.route('/showPasseio')
def showPasseio():
    return render_template('showPasseio.html', passeio=dados_passeio['passeio'])


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return render_template('Block.html', error=500)


# or, without the decorator
app.register_error_handler(500, handle_bad_request)

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "p", ["port="])
    except getopt.GetoptError:
        print('Entre com alguma porta!!!')
        sys.exit(2)
    app.run(host='0.0.0.0', port=args[0])


if __name__ == "__main__":
    main(sys.argv[1:])


