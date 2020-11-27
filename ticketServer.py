import Pyro5.api
import Pyro5.server
import json
import datetime

@Pyro5.api.expose
class Tickets(object):
    tickets = []
    def getTickets(self, data):
        if data['action'] == 'passagem':
            return self.filterTickets(tickets, data['dataIda'], data['dataVolta'], data['paraAeroporto'])
        if data['action'] == 'reservar':
            return data

    def filterTickets(self, tickets, ida, volta, aeroporto):
        rListIda = []
        rListVolta = []
        for t in tickets:

            if t['paraAeroporto'] == aeroporto and datetime.datetime.strptime(t['diaIda'],
                                                                          "%d/%m/%Y") == datetime.datetime.strptime(ida,
                                                                                                                    '%Y-%m-%d'):
                rListIda.append(t)

            elif t['deAeroporto'] == aeroporto and datetime.datetime.strptime(t['diaIda'],
                                                                          "%d/%m/%Y") == datetime.datetime.strptime(
            volta, '%Y-%m-%d'):
                rListVolta.append(t)

        return {'ida': rListIda, 'volta': rListVolta}


daemon = Pyro5.server.Daemon()  
ns = Pyro5.api.locate_ns(port=5050) 
uri = daemon.register(Tickets)  
ns.register("ticketServer.tp2", uri) 
with open('tickets/aeroportos.json') as json_file:
    tickets = json.load(json_file)
Tickets.tickets = tickets
print("Ready.")
daemon.requestLoop()
