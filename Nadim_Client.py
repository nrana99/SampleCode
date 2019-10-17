import socket
import sys

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 4000

    try:
        soc.connect((host, port))
    except:
        print("Connection error")
        sys.exit()

    print("Enter 'terminate' to exit")
    message = input(" -> ")

    while message != 'terminate':
        soc.sendall(message.encode("ascii"))
        if soc.recv(50).decode("ascii") == "-EXIT-":
            sys.exit()
        message = input(" -> ")

    soc.send(b'terminate')

if __name__ == "__main__":
    main()