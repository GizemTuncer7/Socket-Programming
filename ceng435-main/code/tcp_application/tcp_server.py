import socket

HOST = "server"  # server's IP
PORT = 8000

def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # This line is necessary to reuse the port, otherwise experiments may gone wrong
        s.bind((HOST, PORT))                                    # Below is the same as the example
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break

if __name__ == "__main__":
    tcp_server()