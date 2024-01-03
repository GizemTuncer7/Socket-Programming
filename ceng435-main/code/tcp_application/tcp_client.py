import socket
import os

HOST = socket.gethostbyname("server")  # or directly set the server's IP
PORT = 8000

def send_file(client_socket, file_path):
    # 'rb' means that the data read from the file is of type 'bytes'. THis is binary mode
    file_path = os.path.join('/root', 'objects', file_path) 
    with open(file_path, 'rb') as file:
        while True:
            bytes_read = file.read(1024)
            if not bytes_read:
                break
            client_socket.sendall(bytes_read)
    print(f'Sent {file_path}')


client_socket = socket.socket()
client_socket.connect((HOST, PORT))

# Send each pair of small and large objects
for i in range(10):
    send_file(client_socket, f"small-{i}.obj")
    send_file(client_socket, f"large-{i}.obj")

client_socket.close()
