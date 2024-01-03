import socket
from collections import deque
import Package
import os
import threading
import datetime
import pickle
import struct
import Package

# MACROS
BUFFER_SIZE = 1350
WINDOW_SIZE = 150
tag = 0
data_chunk_list  = []
last_appended_index = 0

serverAddressPort = ("server", 8000)
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

window_lock = threading.Lock()


def interleave_parts(large_file_paths, small_file_paths):
    interleaved = []
    larger_list, smaller_list = (large_file_paths, small_file_paths) if len(large_file_paths) > len(small_file_paths) else (small_file_paths, large_file_paths)

    # Interleave parts from the larger and smaller lists
    for i in range(len(larger_list)):
        interleaved.append(larger_list[i])
        if i < len(smaller_list):
            interleaved.append(smaller_list[i])

    return interleaved

def split_data(interleaved_path_list):
    global tag
    sequence_number = 0
    for interleaved_path in interleaved_path_list:
        with open(interleaved_path, 'rb') as file:
            while True:
                data_chunk = file.read(BUFFER_SIZE)
                if not data_chunk:
                    break
                packet = Package.Package(sequence_number=sequence_number, data_chunk=data_chunk, tag=tag)
                tag += 1
                data_chunk_list.append(packet)
        sequence_number += 1

def get_interleaved_path_list():
    large_file_paths = []
    small_file_paths = []
    for i in range(10):
        large_file_paths.append(os.path.join('/root', 'objects', f"large-{i}.obj"))
        small_file_paths.append(os.path.join('/root', 'objects', f"small-{i}.obj"))

    interleaved_path_list = interleave_parts(large_file_paths, small_file_paths)
    return interleaved_path_list

def fill_the_window():
    global last_appended_index
    while(len(window) < WINDOW_SIZE):
        try:
            packet = data_chunk_list[last_appended_index]
            window.append(packet)
            last_appended_index += 1
        except StopIteration:
            break

def unpack_ack(packed_ack):
    return struct.unpack('!I', packed_ack)[0]

def send_data():
    global window 
    for packet in window:
        if packet.get_state() == "wait":
            packet.change_state_as_sent()
            print(f"Sending packet with sequence number {packet.sequence_number} and tag {packet.tag}")
            packed_package = packet.packed_data_chunk_package()
            UDPClientSocket.sendto(packed_package, serverAddressPort)
        elif packet.get_state() == "sent":
            if packet.is_timeout():
                print(f"Timeout, sequence number = {packet.sequence_number} {packet.tag}")
                packet.sent_time = datetime.datetime.utcnow().timestamp()
                UDPClientSocket.sendto(packet.packed_data_chunk_package(), serverAddressPort)

        

def receive_ack():
    global last_appended_index
    global window
    # Şimdilik ack kısmı bu şekilde dursun sonra package içerisine koyucaz ack kısmını
    ack, address = UDPClientSocket.recvfrom(BUFFER_SIZE)
    ack = unpack_ack(ack)

    for w_packet in window:
        if w_packet.tag == ack:
            w_packet.change_state_as_Acked()
            break
    
    if window[0].get_state() == "acked":
        window.popleft()
        if data_chunk_list[last_appended_index]:
            next_data_chunk = data_chunk_list[last_appended_index]
            last_appended_index += 1
          

interleaved_path_list = get_interleaved_path_list()

split_data(interleaved_path_list)

window = deque(maxlen=WINDOW_SIZE)
fill_the_window()

while True:
    send_data()
    receive_ack()
    

UDPClientSocket.close()