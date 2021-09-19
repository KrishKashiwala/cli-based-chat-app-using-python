import socket
import threading
import datetime

host = "127.0.0.1"
port = 6000
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
    loginTime = datetime.datetime.now().strftime("%X")
    allsockets[name] = client
    loginMsg = "Server: time=" + loginTime + " " + name + " has joined. Member count=" + str(len(allsockets))
    sendAllClients(loginMsg)
    while True:
        chat = client.recv(2040).decode()
        if chat == "quit":
            quitTime = datetime.datetime.now().strftime("%X")
            quitmsg = "Server: time=" + quitTime + " " + name + " has left. Member count=" + str(len(allsockets) - 1)
            del allsockets[name]
            sendAllClients(quitmsg)
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

