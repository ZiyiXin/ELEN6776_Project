from socket import *
import sys


def request_file(filename, server_ip, server_port):
    client_socket = socket(AF_INET, SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))
        client_socket.sendall(filename.encode())

        file_content = ''
        while True:
            response = client_socket.recv(2048)
            if not response:
                break
            file_content += response.decode()
        print(file_content)
    finally:
        client_socket.close()


def print_welcome_message():
    welcome_message = """
###############################################################
#                                                            #
#     Welcome to Cache Simulator by Ziyi Xin and Meng Li!    #
#   Here you can type in the lyrics of OSTs of many TV       #
#   shows you want. Come and try it out!                     #
#                                                            #
###############################################################
"""
    print(welcome_message)


if __name__ == "__main__":
    print_welcome_message()
    server_ip = '127.0.0.1'  # Update with your server IP
    server_port = 8081       # Update with your server port
    while True:
        try:
            filename = input("What do you want to check: ").strip()
            if not filename:
                print("Filename cannot be empty. Please try again.")
                continue
            request_file(filename, server_ip, server_port)
            deter = input("Are you still looking for something else?(y/n): ").strip().lower()
            if deter == "n":
                break
        except KeyboardInterrupt:
            print("\nExiting gracefully.")
            break
        except Exception as e:
            print(f"Wrong attempt, please try again later. Error: {e}")