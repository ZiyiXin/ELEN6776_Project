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

class LFU:
    def __init__(local):
        # maximum file that can be stored in the cache: 10
        local.length = 10
        # dictionary for cached files
        local.cache = {} # {key:value}
        # dictionary to track frequency
        local.frequency = {} # {key:frequency}

    def get_file(local, key, value):
        if key in local.cache:
            local.frequency[key] += 1
            return local.cache[key]
        else:
            if len(local.cache) >= local.length:
                local.delete()
            else:
                local.frequency[key] = 1
                local.cache[key] = value
        
    def delete(local):
        del_key = min(local.frequency, key=local.frequency.get)
        del local.cache[del_key]
        del local.frequency[del_key]



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