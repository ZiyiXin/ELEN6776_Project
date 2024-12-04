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
        file_path = os.path.join('Database', f'{filename}.txt')
        with open(file_path, 'r') as file:
                content = file.read()
        client_socket.sendall(content.encode())

    except Exception:
        print(f'Error')


if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 80

    start_server(HOST, PORT)











# import os
# import socket
# import threading
# import time  # Added for optional delay

# # Server configuration
# HOST = '0.0.0.0'
# PORT = 1234
# BUFFER_SIZE = 1024
# FILES_DIR = "./Database"

# # Simulate the file pool
# server_file = {
#     1: 'one.txt',
#     2: 'two.txt',
#     3: 'three.txt',
#     4: 'four.txt',
#     5: 'five.txt',
#     6: 'six.txt',
#     7: 'seven.txt',
#     8: 'eight.txt',
#     9: 'nine.txt',
#     10: 'ten.txt',
#     11: 'eleven.txt',
#     12: 'twelve.txt',
#     13: 'thirteen.txt',
#     14: 'fourteen.txt',
#     15: 'fifteen.txt',
#     16: 'sixteen.txt',
#     17: 'seventeen.txt',
#     18: 'eighteen.txt',
#     19: 'nineteen.txt',
#     20: 'twenty.txt',
#     21: 'twenty_one.txt',
#     22: 'twenty_two.txt',
#     23: 'twenty_three.txt',
#     24: 'twenty_four.txt',
#     25: 'twenty_five.txt',
#     26: 'twenty_six.txt',
#     27: 'twenty_seven.txt',
#     28: 'twenty_eight.txt',
#     29: 'twenty_nine.txt',
#     30: 'thirty.txt',
#     31: 'thirty_one.txt',
#     32: 'thirty_two.txt',
#     33: 'thirty_three.txt',
#     34: 'thirty_four.txt',
#     35: 'thirty_five.txt',
#     36: 'thirty_six.txt',
#     37: 'thirty_seven.txt',
#     38: 'thirty_eight.txt',
#     39: 'thirty_nine.txt',
#     40: 'forty.txt',
#     41: 'forty_one.txt',
#     42: 'forty_two.txt',
#     43: 'forty_three.txt',
#     44: 'forty_four.txt',
#     45: 'forty_five.txt',
#     46: 'forty_six.txt',
#     47: 'forty_seven.txt',
#     48: 'forty_eight.txt',
#     49: 'forty_nine.txt',
#     50: 'fifty.txt',
#     51: 'fifty_one.txt',
#     52: 'fifty_two.txt',
#     53: 'fifty_three.txt',
#     54: 'fifty_four.txt',
#     55: 'fifty_five.txt',
#     56: 'fifty_six.txt',
#     57: 'fifty_seven.txt',
#     58: 'fifty_eight.txt',
#     59: 'fifty_nine.txt',
#     60: 'sixty.txt',
#     61: 'sixty_one.txt',
#     62: 'sixty_two.txt',
#     63: 'sixty_three.txt',
#     64: 'sixty_four.txt',
#     65: 'sixty_five.txt',
#     66: 'sixty_six.txt',
#     67: 'sixty_seven.txt',
#     68: 'sixty_eight.txt',
#     69: 'sixty_nine.txt',
#     70: 'seventy.txt',
#     71: 'seventy_one.txt',
#     72: 'seventy_two.txt',
#     73: 'seventy_three.txt',
#     74: 'seventy_four.txt',
#     75: 'seventy_five.txt',
#     76: 'seventy_six.txt',
#     77: 'seventy_seven.txt',
#     78: 'seventy_eight.txt',
#     79: 'seventy_nine.txt',
#     80: 'eighty.txt',
#     81: 'eighty_one.txt',
#     82: 'eighty_two.txt',
#     83: 'eighty_three.txt',
#     84: 'eighty_four.txt',
#     85: 'eighty_five.txt',
#     86: 'eighty_six.txt',
#     87: 'eighty_seven.txt',
#     88: 'eighty_eight.txt',
#     89: 'eighty_nine.txt',
#     90: 'ninety.txt',
#     91: 'ninety_one.txt',
#     92: 'ninety_two.txt',
#     93: 'ninety_three.txt',
#     94: 'ninety_four.txt',
#     95: 'ninety_five.txt',
#     96: 'ninety_six.txt',
#     97: 'ninety_seven.txt',
#     98: 'ninety_eight.txt',
#     99: 'ninety_nine.txt',
#     100: 'one_hundred.txt'
# }

# def handle_client(client_socket):
#     try:
#         # Receive the requested filename from the client
#         filename = client_socket.recv(BUFFER_SIZE).decode()
#         filepath = os.path.join(FILES_DIR, filename)
#         print(f"Server received request for file: {filename}")
#         print(f"Checking file at path: {filepath}")

#         # Check if the file exists
#         if os.path.isfile(filepath):
#             # Notify client that the file is found
#             client_socket.send(b"FOUND")
#             print("Server sent 'FOUND' message to client.")
#             time.sleep(0.1)  # Optional: small delay to ensure messages are received in order

#             # Send file size to client
#             file_size = os.path.getsize(filepath)
#             client_socket.send(f"{file_size}".encode())
#             print(f"Server sent file size: {file_size}")

#             # Send the file content in chunks
#             with open(filepath, "rb") as f:
#                 while True:
#                     bytes_read = f.read(BUFFER_SIZE)
#                     if not bytes_read:
#                         break
#                     client_socket.sendall(bytes_read)
#             print(f"File '{filename}' sent to client.")
#         else:
#             # Notify client file was not found
#             client_socket.send(b"NOTFOUND")
#             print(f"File '{filename}' not found in '{FILES_DIR}'. Sent 'NOTFOUND' to client.")

#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         client_socket.close()

# def start_server():
#     if not os.path.exists(FILES_DIR):
#         os.makedirs(FILES_DIR)

#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((HOST, PORT))
#     server_socket.listen(5)
#     print(f"Server started on {HOST}:{PORT}. Waiting for connections...")

#     while True:
#         client_socket, client_address = server_socket.accept()
#         print(f"Client {client_address} connected.")
#         client_handler = threading.Thread(target=handle_client, args=(client_socket,))
#         client_handler.start()

# if __name__ == "__main__":
#     start_server()