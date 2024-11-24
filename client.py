import xmlrpc.client
#import threading
#import time
#import random

coordinator = xmlrpc.client.ServerProxy("http://localhost:50000")

def get(account):
    return coordinator.get(account)

def transfer(source, dest, amount):
    return coordinator.transfer(source, dest, amount)

if __name__ == "__main__":
    print("A: " + str(get("a")))
    print("B: " + str(get("b")))
    print(transfer("a", "b", 50))
    print("A: " + str(get("a")))
    print("B: " + str(get("b")))