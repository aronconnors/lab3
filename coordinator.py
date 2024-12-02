from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
#import os

coordinator = SimpleXMLRPCServer(("localhost", 50000))
participantA = xmlrpc.client.ServerProxy("http://localhost:50001")
participantB = xmlrpc.client.ServerProxy("http://localhost:50002")
clock = 0

def get(account):
    if account == "a":
        return participantA.get()
    elif account == "b":
        return participantB.get()
    else:
        return "Fuck you"
    
def transfer(source, dest, amount):
    global clock
    clock += 1
    if source == "a" and dest == "b" and amount >= 0:
        if participantA.prepare(amount*-1, clock) and participantB.prepare(amount, clock):
            if participantA.commit(amount*-1, clock) and participantB.commit(amount, clock):
                return "success"
            else:
                return "failure1"
        else:
            return "failure2"
    elif source == "b" and dest == "a" and amount >= 0:
        if participantB.prepare(amount*-1, clock) and participantA.prepare(amount, clock):
            if participantB.commit(amount*-1, clock) and participantA.commit(amount, clock):
                return "success"
            else:
                return "failure1"
        else:
            return "failure2"
    else:
        return "Fuck you"


coordinator.register_function(get,"get")
coordinator.register_function(transfer,"transfer")
coordinator.serve_forever()