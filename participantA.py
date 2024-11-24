from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
#import os

coordinator = xmlrpc.client.ServerProxy("http://localhost:50000")
participantA = SimpleXMLRPCServer(("localhost", 50001))
participantB = xmlrpc.client.ServerProxy("http://localhost:50002")

accountA = 100
preparedValue = 0

def get():
    return accountA

def prepare(value):
    global accountA
    global preparedValue
    if accountA + value >= 0:
        preparedValue = value
        return True
    else:
        return False

def commit(value):
    global accountA
    global preparedValue
    if preparedValue == value:
        accountA = accountA + value
        return True
    else:
        return False

participantA.register_function(get,"get")
participantA.register_function(prepare,"prepare")
participantA.register_function(commit,"commit")
participantA.serve_forever()