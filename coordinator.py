from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import socket
import os
import sys
import time

socket.setdefaulttimeout(5.0)
coordinator = SimpleXMLRPCServer(("localhost", 50000))
participantA = xmlrpc.client.ServerProxy("http://localhost:50001")
participantB = xmlrpc.client.ServerProxy("http://localhost:50002")
clock = 0

def get(account):
    try:
        if account == "a":
            return participantA.get()
        elif account == "b":
            return participantB.get()
        else:
            return "Invalid account"
    except (socket.timeout, ConnectionRefusedError, xmlrpc.client.Fault) as e:
        return f"Error retrieving balance for account {account}: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
    
def transfer(source, dest, amount):
    global clock
    clock += 1
    try:
        if source == "a" and dest == "b" and amount >= 0:
            try:
                prepareA = participantA.prepare(amount*-1, clock)
            except (socket.timeout, ConnectionRefusedError, xmlrpc.client.Fault):
                return "Participant A timeout during prepare phase."
            try:
                prepareB = participantB.prepare(amount, clock)
            except (socket.timeout, ConnectionRefusedError, xmlrpc.client.Fault):
                return "Participant B timeout during prepare phase."

            if prepareA and prepareB:
                try:
                    commitA = participantA.commit(amount*-1, clock)
                except (socket.timeout, ConnectionRefusedError, xmlrpc.client.Fault):
                    return "Participant A timeout during commit phase."

                try:
                    commitB = participantB.commit(amount, clock)
                except (socket.timeout, ConnectionRefusedError, xmlrpc.client.Fault):
                    return "Participant B timeout during commit phase."

                if commitA and commitB:
                    return "success"
                else:
                    return "failure during commit phase"
            else:
                return "failure during prepare phase"
        else:
            return "Invalid transfer parameters"
    except Exception as e:
        return f"An error occurred: {e}"


coordinator.register_function(get,"get")
coordinator.register_function(transfer,"transfer")
coordinator.serve_forever()