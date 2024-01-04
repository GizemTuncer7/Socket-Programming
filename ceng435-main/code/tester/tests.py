import os
import socket
from Command_Line_Creator import *

def run_tcp_server():
    tcp_command = f"python3 /root/code/tcp_application/tcp_server.py" 
    os.system(tcp_command)

def run_tcp_client():
    tcp_command = f"python3 /root/code/tcp_application/tcp_client.py" 
    os.system(tcp_command)

def run_udp_server():
    udp_command = f"python3 /root/code/udp_application/udp_server.py" 
    os.system(udp_command)

def run_udp_client():
    udp_command = f"python3 /root/code/udp_application/udp_client.py" 
    os.system(udp_command)

def tester_benchmark():
    print(f"Running the benchmark tester on {socket.gethostname()}")

    command_line_creator = Command_Line_Creator()

    command_line_creator.reset_command()
    command_line_creator.run_command()

    print("Running the UDP client")

    run_udp_client()

    # print("Running the TCP client")

    # run_tcp_client()

    print("Benchmark test is done")

if __name__ == "__main__":
    tester_benchmark()





