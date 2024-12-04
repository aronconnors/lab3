import xmlrpc.client
import subprocess
import time
import os


def reset():
    if os.path.exists('accountA.txt'):
        open('accountA.txt', 'w').close()
    if os.path.exists('accountB.txt'):
        open('accountB.txt', 'w').close()

def startCoordinator():
    return subprocess.Popen(["python3", "coordinator.py"])

def startParticipantA(initialBal, crash=None):
    args = ["python3","participantA.py", str(initialBal)]
    if crash:
        args.append(crash)
    return subprocess.Popen(args)

def startParticipantB(initialBal):
    return subprocess.Popen(["python3","participantB.py",str(initialBal)])

def printBalances(coordinator):
    try:
        ABal = coordinator.get("a")
    except Exception as e:
        ABal = f"Error: {e}"
    try:
        BBal = coordinator.get("b")
    except Exception as e:
        BBal = f"Error: {e}"

    print(f"Account A: {ABal}")
    print(f"Account B: {BBal}")

def end(A,B):
    A.terminate()
    B.terminate()
    time.sleep(1)

def scenarioA(coordinator):
    print("Scenario A:")
    reset()
    #transfer
    participantA = startParticipantA(200)
    participantB = startParticipantB(300)
    time.sleep(1)
    print("transferring 100 from a to b")
    result = coordinator.transfer("a","b",100)
    print(result)
    printBalances(coordinator)
    #bonus
    time.sleep(1)
    print("Bonus transaction")
    result = coordinator.bonus()
    print(result)
    printBalances(coordinator)
    end(participantA,participantB)

def scenarioB(coordinator):
    print("scenario B:")
    reset()
    #transfer
    participantA = startParticipantA(90)
    participantB = startParticipantB(50)
    time.sleep(1)
    print("transferring 100 from a to b")
    result = coordinator.transfer("a","b",100)
    print(result)
    printBalances(coordinator)
    #bonus
    time.sleep(1)
    print("Bonus transaction")
    result = coordinator.bonus()
    print(result)
    printBalances(coordinator)
    end(participantA,participantB)

def scenarioCi(coordinator):
    print("scenario C.i")
    reset()
    participantA = startParticipantA(200, "before_prepare")
    participantB = startParticipantB(300)
    time.sleep(1)
    print("transferring 100 from a to b")
    result = coordinator.transfer("a","b",100)
    print(result)
    printBalances(coordinator)
    #add bonus? not sure if we add them here
    end(participantA,participantB)

def scenarioCii(coordinator):
    print("scenario C.ii")
    reset()
    participantA = startParticipantA(200, "after_prepare")
    participantB = startParticipantB(300)
    time.sleep(1)
    print("transferring 100 from a to b")
    result = coordinator.transfer("a","b",100)
    print(result)
    printBalances(coordinator)
    #add bonus? not sure if we add them here
    end(participantA,participantB) 

if __name__ == "__main__":
    c = startCoordinator()
    time.sleep(1)
    coordinator = xmlrpc.client.ServerProxy("http://localhost:50000")
    while True:
        print("\n1 - Scenario A")
        print("2 - Scenario B")
        print("3 - Scenario C.i")
        print("4 - Scenario C.ii")
        print("exit")
        scen = input("Enter scenario option: ").strip()
        if scen == "1":
            scenarioA(coordinator)
        elif scen == "2":
            scenarioB(coordinator)
        elif scen == "3":
            scenarioCi(coordinator)
        elif scen == "4":
            scenarioCii(coordinator)
        elif scen == "exit":
            c.terminate()
            time.sleep(1)
            break