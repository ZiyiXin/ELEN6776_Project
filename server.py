import os
import socket
import threading
import time  # Added for optional delay

# Server configuration
HOST = '0.0.0.0'
PORT = 1234
BUFFER_SIZE = 1024
FILES_DIR = "./Database"

def handle_client(client_socket):
    try:
        # Receive the requested filename from the client
        filename = client_socket.recv(BUFFER_SIZE).decode()
        filepath = os.path.join(FILES_DIR, filename)
        print(f"Server received request for file: {filename}")
        print(f"Checking file at path: {filepath}")

        # Check if the file exists
        if os.path.isfile(filepath):
            # Notify client that the file is found
            client_socket.send(b"FOUND")
            print("Server sent 'FOUND' message to client.")
            time.sleep(0.1)  # Optional: small delay to ensure messages are received in order

            # Send file size to client
            file_size = os.path.getsize(filepath)
            client_socket.send(f"{file_size}".encode())
            print(f"Server sent file size: {file_size}")

            # Send the file content in chunks
            with open(filepath, "rb") as f:
                while True:
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    client_socket.sendall(bytes_read)
            print(f"File '{filename}' sent to client.")
        else:
            # Notify client file was not found
            client_socket.send(b"NOTFOUND")
            print(f"File '{filename}' not found in '{FILES_DIR}'. Sent 'NOTFOUND' to client.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_server():
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server started on {HOST}:{PORT}. Waiting for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Client {client_address} connected.")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()