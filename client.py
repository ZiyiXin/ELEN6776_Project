import os
import socket

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 1234
BUFFER_SIZE = 2048

# Directory to save downloaded files
DOWNLOADS_DIR = "./Clients"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

def request_file(filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    try:
        # Send the filename request to the server
        print(f"Client sending filename: {filename}")
        client_socket.send(filename.encode())

        # Receive response from the server (FOUND or NOTFOUND)
        response = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Client received response: {response}")
        
        if response == "FOUND":
            # Receive file size from the server
            file_size = int(client_socket.recv(BUFFER_SIZE).decode())
            print(f"Client received file size: {file_size} bytes. Downloading...")

            # Set the path to save the downloaded file in the downloads directory
            download_path = os.path.join(DOWNLOADS_DIR, filename)

            # Open the file to write the received content
            with open(download_path, "wb") as f:
                bytes_received = 0
                while bytes_received < file_size:
                    bytes_read = client_socket.recv(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
                    bytes_received += len(bytes_read)
                    print(f"Received {bytes_received}/{file_size} bytes...")  # Progress output

            if bytes_received == file_size:
                print(f"File '{filename}' downloaded successfully to '{DOWNLOADS_DIR}'.")
            else:
                print(f"Download incomplete. Expected {file_size} bytes, received {bytes_received} bytes.")
        else:
            print(f"File '{filename}' not found on the server.")
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    filename = input("Enter the filename to request: ")
    request_file(filename)