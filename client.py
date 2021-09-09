import socket
from threading import Thread
from datetime import datetime

host = "127.0.0.1"
port = 9999
separator = "<SEP>"

s = socket.socket()
print(f"Connecting to {host}:{port}...")
s.connect((host, port))
print(f"Connected to {host}")
name = input("Enter your name: ")


def listern_for_message():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)


t = Thread(target=listern_for_message)
t.daemon = True
t.start()
while True:
    to_send = input()
    if to_send.lower() == 'q':
        break
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    to_send = f"{date_now} {name}{separator}{to_send}"
    s.send(to_send.encode())
s.close()