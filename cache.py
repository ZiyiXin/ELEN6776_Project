# ========================================================
from socket import *
import select
import threading
import os
import shutil
# import time

# ========================================================
# define everything used within Least Frequently Used algorighm
class LFU:
    # Initiate the class
    def __init__(self, max_length, cache_dir):
        # maximum file that can be stored in the cache: 10
        self.length = max_length
        self.cache = {} # store file path
        self.frequency = {} # track frequency
        self.cache_dir = cache_dir

        # ensure local storage exists
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        else:
            # 清空 cache 目录中的所有文件
            self.clear_cache()

    def clear_cache(self):
        """清空 cache 目录中的所有文件"""
        for filename in os.listdir(self.cache_dir):
            file_path = os.path.join(self.cache_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  
        print(f"Cache directory '{self.cache_dir}' has been cleared.")

    # get the file from cache based on client requests
    def get_file(self, key):
        if key in self.cache:
            self.frequency[key] += 1
            file_path = self.cache[key]
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    return f.read()

        return None
    
    # delete least frequently used files  
    def del_file(self):
        del_key = min(self.frequency, key=self.frequency.get) # find least frequently used file
        file_path = self.cache[del_key]
        
        if os.path.exists(file_path):
            os.remove(file_path)
        del self.cache[del_key]
        del self.frequency[del_key]
    
    # add file to cache 
    def add_file(self, key, content):
        if len(self.cache) >=  self.length:
            self.del_file()

        file_name = f"{key}.txt"
        file_path = os.path.join(self.cache_dir,file_name) 
        with open(file_path, 'wb') as f:
            f.write(content.encode())
        
        self.cache[key] = file_path
        self.frequency[key] = 1

# executing the proxy
def start_proxy(listen_port, server_ip, server_port):
    # Socket that the proxy used to listen for incoming connection
    # e.g. Client
    global cache

    cache = LFU(max_length=3, cache_dir="cache")


    proxy_socket = socket(AF_INET, SOCK_STREAM)
    proxy_socket.bind(('', listen_port))
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
                target = proxy,
                args=(client_socket, server_socket)
            ).start()
    except KeyboardInterrupt:
        print("Proxy shutting down.")
    finally:
        proxy_socket.close()

# main proxy logic
def proxy(client_socket, server_socket):
    global cache
    try:
        while True:
            readable_sockets, _, _ = select.select([client_socket, server_socket], [], [])
            
            for i in readable_sockets:
                # data from client
                if i == client_socket:
                    key = client_socket.recv(2048).decode()
                    if not key:
                        print("Client disconnected.")
                        return None

                    cache_file = cache.get_file(key)
                    if cache_file:
                        print(f'Cache hit: {key}')
                        client_socket.sendall(cache_file)
                    else:
                        print(f'Cache miss: {key}. Sending to server...')
                        server_socket.sendall(key.encode())
                
                # receiving data from server
                elif i == server_socket:
                    content = ''
                    value = server_socket.recv(2048).decode()
                    client_socket.sendall(value.encode())
                        
                    print(f'Caching response from server: {key}')
                    cache.add_file(key,value)
    except Exception as e:
        print(f'Error: {e}')
    finally:
        client_socket.close()
        server_socket.close()
        print("Closed client-server session.")

if __name__ == "__main__":
    LISTEN_PORT = 8081

    # server is hosted locally.
    SERVER_IP = "127.0.0.1"
    
    # by default, set it to 8080
    SERVER_PORT = 8080

    start_proxy(LISTEN_PORT, SERVER_IP, SERVER_PORT)

