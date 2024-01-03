import socket

HOST = "server"  # server's IP
PORT = 8000

#def receive_file(connection, file_name):
#    with open(file_name, 'wb') as file:
#        while True:
#            data = connection.recv(1024)
#            if not data:
#                break
#            file.write(data)
#    print(f'Received {file_name}')

# echo-server.py

# You have to implement threading for handling multiple TCP connections
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break