import Pyro5.api
import Pyro5.server
import json
import datetime

@Pyro5.api.expose
class Passeios(object):
    passeios = []
    def getPasseios(self, data):
        return self.filterPasseios(passeios, data['dataIda'], data['cidade'])

    def filterPasseios(self, passeio, ida, cidade):
        rListPass = []
       
        for p in passeio:
            if p['cidade'] in cidade or p['endereco'] in cidade:
                if datetime.datetime.strptime(p['dia'], "%d/%m/%Y") == datetime.datetime.strptime(ida, '%Y-%m-%d'):
                    rListPass.append(p)
        return {'passeio': rListPass}


daemon = Pyro5.server.Daemon()  
ns = Pyro5.api.locate_ns(port=5050)  
uri = daemon.register(Passeios)  
ns.register("passeioServer.tp2", uri) 
with open('tickets/passeios.json') as json_file:
    passeios = json.load(json_file)
Passeios.passeios = passeios
print("Ready.")
daemon.requestLoop()
