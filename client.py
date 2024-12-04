import xmlrpc.client
import time

def start(aValue, bValue, crash):
    return coordinator.start(aValue, bValue, crash)
    
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

def scenarioA(coordinator):
    print("Scenario A:")
    start(200, 300, 'no_crash')
    #transfer
    time.sleep(1)
    printBalances(coordinator)
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

def scenarioB(coordinator):
    print("scenario B:")
    #transfer
    start(90, 50, 'no_crash')
    time.sleep(1)
    printBalances(coordinator)
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

def scenarioCi(coordinator):
    print("scenario C.i")
    #reset()
    start(200, 300, "before_prepare")
    time.sleep(1)
    printBalances(coordinator)
    time.sleep(1)
    print("transferring 100 from a to b")
    result = coordinator.transfer("a","b",100)
    print(result)
    printBalances(coordinator)

def scenarioCii(coordinator):
    print("scenario C.ii")
    start(200, 300, "after_prepare")
    time.sleep(1)
    printBalances(coordinator)
    time.sleep(1)
    print("transferring 100 from a to b")
    result = coordinator.transfer("a","b",100)
    print(result)
    printBalances(coordinator)

if __name__ == "__main__":
    coordinator = xmlrpc.client.ServerProxy("http://localhost:50000", allow_none=True)
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
            time.sleep(1)
            break