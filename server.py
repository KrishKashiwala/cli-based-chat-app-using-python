import socket
import threading
import datetime

host = "127.0.0.1"
port = 6001
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)
allsockets = {}
allthreads = []


def sendAllClients(msg, dontSendTo="None"):
    for t in allsockets.keys():
        if t == dontSendTo:
            continue
        allsockets[t].send(msg.encode("UTF-8"))


def onNewClient(client):
    name = client.recv(2040).decode()
    allsockets[name] = client
    log_msg = name + " has joined. Total members : " + str(len(allsockets))
    sendAllClients(log_msg)
    while True:
        chat = client.recv(2040).decode()
        if chat == "quit":
            quit_msg = name + " has left. Total members : " + str(len(allsockets) - 1)
            del allsockets[name]
            sendAllClients(quit_msg)
            client.send("qqqqq".encode("UTF-8"))
            client.close()
            break
        else:
            chat = name + ": " + chat
            sendAllClients(chat, name)


while True:
    client, addr = server.accept()
    t = threading.Thread(target=onNewClient, args=(client,))
    allthreads.append(t)
    t.start()
