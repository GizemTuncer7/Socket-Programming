import os
import time

def run_servers():
    os.system("python3 /root/code/udp_application/udp_server.py")

    time.sleep(1)

    # os.system("python3 /root/code/tcp_application/tcp_server.py")

    # time.sleep(1)

if __name__ == "__main__":
    run_servers()
    print("Servers are running")
    