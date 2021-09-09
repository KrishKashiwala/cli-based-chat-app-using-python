import socket
from threading import Thread

host = ""
port = 9999

separator = "<SEP>"
# initialize all list of users
client_sockets = set()


def create_socket():
    s = socket.socket()
    # make a port reusable
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    print(f"Server is listening for {host}:{port}.")
    while True:
        client_socket, client_address = s.accept()
        print(f"{client_address} connected.")
        client_sockets.add(client_socket)
        # start a thread that listerns to users message
        t = Thread(target=listern_for_client, args=(client_socket,))
        t.daemon = True
        t.start()
    s.close()


def listern_for_client(cs):
    while True:
        try:
            msg = cs.recv(1024).decode()
        except Exception as e:
            print(f"Error {e} has occurred.")
            client_sockets.remove(cs)
        else:
            msg = msg.replace(separator, ":")

        for client_socket in client_sockets:
            client_socket.send(msg.encode())
    for cs in client_sockets:
        cs.close()


create_socket()