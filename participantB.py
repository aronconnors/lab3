from xmlrpc.server import SimpleXMLRPCServer
import os

participantB = SimpleXMLRPCServer(("localhost", 50002), allow_none=True)

accountFile = "accountB.txt"
preparedValue = 0
clockValue = 0

def start(initialBal):
    global accountFile
    with open(accountFile, 'w') as f:
        f.write(str(initialBal))
    preparedValue = 0
    clockValue = 0
    return 'success'

def readAccount():
    if os.path.exists(accountFile):
        with open(accountFile, 'r') as f:
            return int(f.read())
    else:
        return "Problem"

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

participantB.register_function(start,"start")
participantB.register_function(get,"get")
participantB.register_function(prepare,"prepare")
participantB.register_function(commit,"commit")
participantB.serve_forever()