from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
#import os

coordinator = SimpleXMLRPCServer(("localhost", 50000))
participantA = xmlrpc.client.ServerProxy("http://localhost:50001")
participantB = xmlrpc.client.ServerProxy("http://localhost:50002")

def get(account):
    if account == "a":
        return participantA.get()
    elif account == "b":
        return participantB.get()
    else:
        return "Fuck you"
    
def transfer(source, dest, amount):
    if source == "a" and dest == "b" and amount >= 0:
        if participantA.prepare(amount*-1) and participantB.prepare(amount):
            if participantA.commit(amount*-1) and participantB.commit(amount):
                return "success"
            else:
                return "failure1"
        else:
            return "failure2"
    elif source == "b" and dest == "a" and amount >= 0:
        if participantB.prepare(amount*-1) and participantA.prepare(amount):
            if participantB.commit(amount*-1) and participantA.commit(amount):
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