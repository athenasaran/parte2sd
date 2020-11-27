import Pyro5.api
import Pyro5.server
import json
import datetime

@Pyro5.api.expose
class Hosps(object):
    hosps = []
    def getHosps(self, data):
        if data['action'] == 'hospedar':
            return self.filterHosps(hosps, data['dataIda'], data['cidade'], data['numeroDePessoas'])
        if data['action'] == 'reservar':
            return data

    def filterHosps(self, hosps, ida, cidade, pessoas):
        rListHosp = []
        for h in hosps:
            if h['cidade'] == cidade:
                if ((datetime.datetime.strptime(h['diaEntrada'], "%d/%m/%Y") == datetime.datetime.strptime(ida,'%Y-%m-%d')) & (int(h['qtdCamas']) >= int(pessoas))):
                    rListHosp.append(h)
        return {'hospedagens': rListHosp}


daemon = Pyro5.server.Daemon()  
ns = Pyro5.api.locate_ns(port=5050)  
uri = daemon.register(Hosps)  
ns.register("hospServer.tp2", uri)  
with open('tickets/hospedagens.json') as json_file:
    hosps = json.load(json_file)
Hosps.hosps = hosps
print("Ready.")
daemon.requestLoop()
