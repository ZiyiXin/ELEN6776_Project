# Server for dict simulation

from socket import *
import os

# Simulated File Storage
# TODO: complete file storage
FILE_STORAGE = {
    "friends":"firends.txt", 
    "frozen":"frozen.txt", 
    "himym":"himym.txt", 
    "pony":"pony.txt", 
    "shameless":"shameless.txt", 
    "spiderman":"spiderman.txt", 
    "tbbt":"tbbt.txt", 
    "zootopia":"zootopia.txt"
}


def start_server(host, port):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    try:
        while True:
            client_socket, client_addr = server_socket.accept()

            server(client_socket)
    
    except KeyboardInterrupt:
        print("Server Shutting Down.")

    finally:
        server_socket.close()

def server(client_socket):
    try:
        while True:
            data = client_socket.recv(2048)
            if not data:
                print("Client disconnected.")
                break

            requested_file = data.decode().lower()
            if requested_file in FILE_STORAGE:
                send_file(client_socket, requested_file)
            else:
                message = f"ERROR: '{requested_file}' not found."
                client_socket.send(message.encode())
    except Exception:
        print(f"Error")
    finally:
        client_socket.close()

def send_file(client_socket, file_key):
    try:
        filename = FILE_STORAGE[file_key]
        file_path = os.path.join('Database', f'{filename}')
        with open(file_path, 'r') as file:
                content = file.read()
        client_socket.sendall(content.encode())

    except Exception:
        print(f'Error when sending file')

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 8080

    start_server(HOST, PORT)

