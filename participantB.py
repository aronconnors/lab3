from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import os
import sys
import time

coordinator = xmlrpc.client.ServerProxy("http://localhost:50000")
participantA = xmlrpc.client.ServerProxy("http://localhost:50001")
participantB = SimpleXMLRPCServer(("localhost", 50002), logRequests=False)

accountFile = "accountB.txt"

if len(sys.argv) > 1:
    initialBal = int(sys.argv[1])
    with open(accountFile, 'w') as f:
            f.write(str(initialBal))
else:
    initialBal = 100

preparedValue = 0
clockValue = None

def readAccount():
    if os.path.exists(accountFile):
        with open(accountFile, 'r') as f:
            return int(f.read())

def writeAccount(value):
    with open(accountFile, 'w') as f:
        f.write(str(value))
        
def get():
    return readAccount()

def prepare(value, clock):
    global preparedValue
    global clockValue
    accountB = readAccount()

    if accountB + value >= 0:
        preparedValue = value
        clockValue = clock
        return True
    else:
        return False

def commit(value, clock):
    global preparedValue
    global clockValue

    if preparedValue == value and clockValue == clock:
        accountB = readAccount()
        accountB = accountB + value
        writeAccount(accountB)
        return True
    else:
        return False

participantB.register_function(get,"get")
participantB.register_function(prepare,"prepare")
participantB.register_function(commit,"commit")
participantB.serve_forever()