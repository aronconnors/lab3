from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
#import os

coordinator = xmlrpc.client.ServerProxy("http://localhost:50000")
participantA = SimpleXMLRPCServer(("localhost", 50001))
participantB = xmlrpc.client.ServerProxy("http://localhost:50002")

accountA = 100
preparedValue = 0
clockValue = None

def get():
    return accountA

def prepare(value, clock):
    global accountA
    global preparedValue
    global clockValue
    if accountA + value >= 0:
        preparedValue = value
        clockValue = clock
        return True
    else:
        return False

def commit(value, clock):
    global accountA
    global preparedValue
    global clockValue
    if preparedValue == value and clockValue == clock:
        accountA = accountA + value
        return True
    else:
        return False

participantA.register_function(get,"get")
participantA.register_function(prepare,"prepare")
participantA.register_function(commit,"commit")
participantA.serve_forever()