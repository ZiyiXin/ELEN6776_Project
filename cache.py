# ========================================================
from socket import *
import select
import threading
import sys
import time
# ========================================================
# local storage
cache = {}


# ========================================================
def setup_socekt(address, port):
    s = socket(AF_INET, SOCK_STREAM)
    # as a server
    if address == '':
        s.bind('', port)
        s.listen(200)
    # as a client
    else:
        s.connect((address, port))

def LFU(temp):
    return None

def check_cache(x, cache, client_socket, server_socekt):
    if x in cache:
        return cache[x]
    else:
        server_socekt.send(x)
        response = server_socekt.response(2048)
        if response:
            cache[x] = response
            client_socket.send(response)
        else:
            print("No such file exists")
            return None


def proxy(client_socket, server_socket, server_ip):
    global cache
    try:
        while 1 == 1:
            readable, _, _ = select.select([client_socket, server_socket], [], [])

            # connection from client
            if client_socket in readable:
                data = client_socket.recv(2048)
                if not data:
                    print("Client connection lost")
                    return
                check_cache(data, cache, client_socket, server_socket)
                



    finally:
        client_socket.close()
        server_socket.close()