# ========================================================
from socket import *
import select
import threading
# import sys
# import time

# ========================================================
# define everything used within Least Frequently Used algorighm
class LFU:
    # Initiate the class
    def __init__(self, max_length = 10):
        # maximum file that can be stored in the cache: 10
        self.length = max_length
        

    # get the file from cache
    def get_file(self, key):
        if key in self.cache:
            self.frequency[key] += 1
            return self.cache[key]
        return None
    
    # delete least frequently used files  
    def del_file(self):
        del_key = min(self.frequency, key=self.frequency.get)
        del self.cache[del_key]
        del self.frequency[del_key]
    # add file to cache
    
    def add_file(self, key, value):
        if len(self.cache) >=  self.length:
            self.del_file()
        self.cache[key] = value
        self.frequency[key] += 1

# executing the proxy
def start_proxy(listen_port, server_ip, server_port):
    # Socket that the proxy used to listen for incoming connection
    # e.g. Client
    global cache

    cache = LFU(max_length=10)


    proxy_socket = socket(AF_INET, SOCK_STREAM)
    proxy_socket.bind('', listen_port)
    proxy_socket.listen(100)
    print(f'Proxy server listening on port {listen_port}...')

    try:
        while True:
            client_socket, client_addr = proxy_socket.accept()
            print(f'Accepted connection from {client_addr}')

            try:
                server_socket = socket(AF_INET, SOCK_STREAM)
                server_socket.connect((server_ip, server_port))
            except Exception as e:
                client_socket.close()
                continue

            threading.Thread(
                target = proxy_connection,
                args=(client_socket, server_socket)
            ).start
    except KeyboardInterrupt:
        print("Proxy shutting down.")
    finally:
        proxy_socket.close()

# main proxy logic
def proxy(client_socket, server_socket):
    global cache
    try:
        while True:
            readable_sockets, _, _ = select.select([client_socket, select], [], [])
            
            for i in readable_sockets:
                # data from client
                if i == client_socket:
                    key = client_socket.recv(2048).decode()
                    if not key:
                        print("Disconnected.")
                        return

                    cache_file = cache.get_file(key)
                    if cache_file:
                        print(f'Cache hit: {key}')
                        client_socket.send(cache_file)
                    else:
                        print(f'Cache miss: {key}. Sending to server...')
                        server_socket.send(key.encode())
                
                # receiving data from server
                elif i == server_socket:
                    value = server_socket.recv(2048)
                    if not value:
                        print("Server disconnected.")
                        return
                    
                    print(f'Caching response from server: {key}')
                    cache.add_file(key, value)
                    client_socket.send(value)
    except Exception:
        print(f'Error')
    finally:
        client_socket.close()
        server_socket.close()
        print("Closed client-server session.")

if __name__ == "__main__":
    LISTEN_PORT = 8080

    # server is hosted locally.
    SERVER_IP = "127.0.0.1"
    
    # by default, set it to 80
    SERVER_PORT = 80

    start_proxy(LISTEN_PORT, SERVER_IP, SERVER_PORT)

