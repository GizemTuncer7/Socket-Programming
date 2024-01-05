import socket
import os
import time

HOST = socket.gethostbyname("server")  # or directly set the server's IP
PORT = 8000

def send_file(client_socket, file_path):
    file_path = os.path.join('/root', 'objects', file_path) # Gets the absolute path of the file 
    with open(file_path, 'rb') as file:
        while True:
            bytes_read = file.read(1024)                    # Read 1024 bytes at a time, same as the example
            if not bytes_read:
                break                                       # If there is no bytes left, exist the loop
            client_socket.sendall(bytes_read)


if __name__ == "__main__":
    now = time.time()                                       # Start time for total execution time for sending 20 files

    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))

    for i in range(10):                                     # Send 10 small and 10 large files one by one 
        send_file(client_socket, f"small-{i}.obj")
        send_file(client_socket, f"large-{i}.obj")

    client_socket.close()

    end = time.time()
    elapsed = end - now

    print(f"{elapsed}")                                     # Prints the total execution time, necessary for the plots
