from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
#import os

coordinator = xmlrpc.client.ServerProxy("http://localhost:50000")
participantA = xmlrpc.client.ServerProxy("http://localhost:50001")
participantB = SimpleXMLRPCServer(("localhost", 50002))

accountB = 100
preparedValue = 0
clockValue = None

def get():
    return accountB

def prepare(value, clock):
    global accountB
    global preparedValue
    global clockValue
    if accountB + value >= 0:
        preparedValue = value
        clockValue = clock
        return True
    else:
        return False

def commit(value, clock):
    global preparedValue
    global accountB
    global clockValue
    if preparedValue == value and clockValue == clock:
        accountB = accountB + value
        return True
    else:
        return False

participantB.register_function(get,"get")
participantB.register_function(prepare,"prepare")
participantB.register_function(commit,"commit")
participantB.serve_forever()