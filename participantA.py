from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import os
import sys
import time

#coordinator = xmlrpc.client.ServerProxy("http://10.128.0.16:50000")
participantA = SimpleXMLRPCServer(("10.128.0.17", 50001), allow_none=True)
#participantB = xmlrpc.client.ServerProxy("http://localhost:50002")

accountFile = "accountA.txt"

simulateCrash = ""

def start(initialBal, crash):
    global accountFile
    global simulateCrash
    with open(accountFile, 'w') as f:
        f.write(str(initialBal))
    simulateCrash = crash
    preparedValue = 0
    clockValue = 0
    return 'success'

preparedValue = 0
clockValue = 0

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

    if simulateCrash == "before_prepare":
        print("ParticipantA: simulating crash prior to prepare")
        time.sleep(6)
    accountA = readAccount()
    if accountA + value >= 0:
        preparedValue = value
        clockValue = clock
        if simulateCrash == "after_prepare":
            print("ParticipantA: simulating crash after prepare")
            time.sleep(6)
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

participantA.register_function(start,"start")
participantA.register_function(get,"get")
participantA.register_function(prepare,"prepare")
participantA.register_function(commit,"commit")
participantA.serve_forever()