import socket
import threading

host = "127.0.0.1"
port = 6000
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((host, port))
user = input("Enter your name:")
connection.send(user.encode("UTF-8"))


def chat():
    while True:
        print(user," : ",end="")
        msg = input()
        connection.send(msg.encode("UTF-8"))
        if msg == "quit":
            print("You have successfully logged out")
            break


def msg_from_server():
    while True:
        server_msg = connection.recv(2040).decode()
        if server_msg != "qqqqq":
            print(server_msg)
        else:
            break


t1 = threading.Thread(target=msg_from_server)
t2 = threading.Thread(target=chat)
t1.start()
t2.start()
t1.join()
t2.join()
connection.close()
