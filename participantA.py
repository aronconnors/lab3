from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import os
import sys
import time

coordinator = xmlrpc.client.ServerProxy("http://localhost:50000")
participantA = SimpleXMLRPCServer(("localhost", 50001), logRequests=False)
participantB = xmlrpc.client.ServerProxy("http://localhost:50002")

accountFile = "accountA.txt"

#Checking if there is a file/inputted account value
if len(sys.argv) > 1:
    initialBal = int(sys.argv[1])
    with open(accountFile, 'w') as f:
            f.write(str(initialBal))
else:
    initialBal = 100

if len(sys.argv) > 2:
    crash = sys.argv[2]
else:
    crash = None


preparedValue = 0
clockValue = None

def readAccount():
    if os.path.exists(accountFile):
        with open(accountFile, 'r') as f:
            return int(f.read())
    else:
        with open(accountFile, 'w') as f:
            f.write(str(initialBal))
        return initialBal

def writeAccount(value):
    with open(accountFile, 'w') as f:
        f.write(str(value))

def get():
    return readAccount()

def prepare(value, clock):
    global preparedValue
    global clockValue

    if crash == "before_prepare":
        print("ParticipantA: simulating crash prior to prepare")
        time.sleep(60)
    accountA = readAccount()
    if accountA + value >= 0:
        preparedValue = value
        clockValue = clock
        if crash == "after_prepare":
            print("ParticipantA: simulating crash after prepare")
            time.sleep(60)
        return True
    else:
        return False

def commit(value, clock):
    global preparedValue
    global clockValue
    if preparedValue == value and clockValue == clock:
        accountA = readAccount()
        accountA = accountA + value
        writeAccount(accountA)
        return True
    else:
        return False

participantA.register_function(get,"get")
participantA.register_function(prepare,"prepare")
participantA.register_function(commit,"commit")
participantA.serve_forever()