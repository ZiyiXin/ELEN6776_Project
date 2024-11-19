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
# set up socket connection
def setup_socekt(address, port):
    s = socket(AF_INET, SOCK_STREAM)
    # as a server
    if address == '':
        s.bind('', 80)
        s.listen(200)
    # as a client
    else:
        s.connect((address, port))

# define everything used within Least Frequently Used algorighm
class LFU:
    # Initiate the class
    def __init__(local):
        # maximum file that can be stored in the cache: 10
        local.length = 10
        # dictionary for cached files
        local.cache = {} # {key:value}
        # dictionary to track frequency
        local.frequency = {} # {key:frequency}

    # get the file from cache, update frequency & delete files
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

    # delete least frequently used files  
    def delete(local):
        del_key = min(local.frequency, key=local.frequency.get)
        del local.cache[del_key]
        del local.frequency[del_key]

# check if file stored in cache
def check_cache(x, cache, client_socket, server_socekt):
    if x in cache:
        return True
    else:
        return False

# main proxy behavior
def proxy(client_socket, server_socket):
    global cache
    try:
        while 1 == 1:
            readable, _, _ = select.select([client_socket, server_socket], [], [])

            # message from client
            if client_socket in readable:
                key = client_socket.recv(2048)
                if not key:
                    print("Client connection lost")
                    return
                
                if check_cache(key, cache, client_socket, server_socket):
                    file = cache[key]
                    client_socket.sendto(file)
                else:
                    server_socket.sendto(key)

            # message from server
            if server_socket in readable:
                val = server_socket.recv(2048)
                cache[key] = val
                client_socket.sendto(val)

    finally:
        client_socket.close()
        server_socket.close()

# executing the proxy
def run_proxy(listen_port, server_ip, server_port):
    client = setup_socekt('', listen_port )

    while 1 == 1:
        try:
            client_socket, _ = client.accpet()
            server_socket = setup_socekt(server_ip, server_port)

            t = threading.Thread(target=proxy, args=(client_socket, server_socket, server_ip))

            t.start()
        except KeyboardInterrupt:
            print("Proxy shutting down.")