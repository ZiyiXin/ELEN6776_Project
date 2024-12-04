from socket import *
import sys


def request_file(filename, server_ip, serverPort):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_ip, serverPort))

    client_socket.sendall(filename.encode())

    file_content = ''
    while True:
        response = client_socket.recv(2048)
        if not response:
            break
        file_content += response.decode()
    print(file_content)


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
    while True:
        try:
            filename = input("What do you what to check: ")
            request_file(filename, server_ip='', listen_port=int(8080))
            deter = input("Are you still looking for something else?(y/n): ")
            if deter.lower() == "n":
                break
        except KeyboardInterrupt:
            print("\nExiting gracefully.")
            break
        except Exception as e:
            print(f"Wrong attempt, please try again later. Error: {e}")
