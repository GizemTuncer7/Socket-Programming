import socket
from collections import deque
import Package
import os
import datetime
import struct
import Package

# MACROS
BUFFER_SIZE = 1350
WINDOW_SIZE = 150


class UDP_with_Selective_Repeat:
    window = None
    tag = None
    data_chunk_list  = None
    last_appended_index = None
    is_finished = None
    serverAddressPort = None
    UDPClientSocket = None

    def __init__(self):
        self.window = deque(maxlen=WINDOW_SIZE)
        self.tag = 0
        self.data_chunk_list  = []
        self.last_appended_index = 0
        self.is_finished = False
        self.serverAddressPort = ("server", 8000)
        self.UDPClientSocket = None

    def interleave_parts(self, large_file_paths, small_file_paths):
        interleaved = []
        larger_list, smaller_list = (large_file_paths, small_file_paths) if len(large_file_paths) > len(small_file_paths) else (small_file_paths, large_file_paths)

        # Interleave parts from the larger and smaller lists
        for i in range(len(larger_list)):
            interleaved.append(larger_list[i])
            if i < len(smaller_list):
                interleaved.append(smaller_list[i])

        return interleaved

    def split_data(self, interleaved_path_list):
        sequence_number = 0
        for interleaved_path in interleaved_path_list:
            with open(interleaved_path, 'rb') as file:
                while True:
                    data_chunk = file.read(BUFFER_SIZE)
                    if not data_chunk:
                        break
                    packet = Package.Package(sequence_number=sequence_number, data_chunk=data_chunk, tag=self.tag)
                    self.tag += 1
                    self.data_chunk_list.append(packet)
            sequence_number += 1

    def get_interleaved_path_list(self):
        large_file_paths = []
        small_file_paths = []
        for i in range(10):
            large_file_paths.append(os.path.join('/root', 'objects', f"large-{i}.obj"))
            small_file_paths.append(os.path.join('/root', 'objects', f"small-{i}.obj"))

        interleaved_path_list = self.interleave_parts(large_file_paths, small_file_paths)
        return interleaved_path_list

    def fill_the_window(self):
        while(len(self.window) < WINDOW_SIZE):
            try:
                packet = self.data_chunk_list[self.last_appended_index]
                self.window.append(packet)
                self.last_appended_index += 1
            except StopIteration:
                break

    def unpack_ack(self, packed_ack):
        return struct.unpack('!I', packed_ack)[0]

    def send_data(self):
        print("Window length:", len(self.window))
        if (len(self.window) == 0):
            print("VALLA BITTI")
            self.is_finished = True
            print("VALLA BITTI: ", self.is_finished)

        for packet in self.window:
            if packet.get_state() == "wait":
                packet.change_state_as_sent()
                print(f"Sending packet with sequence number {packet.sequence_number} and tag {packet.tag}")
                packed_package = packet.packed_data_chunk_package()
                self.UDPClientSocket.sendto(packed_package, self.serverAddressPort)
            elif packet.get_state() == "sent":
                if packet.is_timeout():
                    # print(f"Timeout, sequence number = {packet.sequence_number} {packet.tag}")
                    packet.sent_time = datetime.datetime.utcnow().timestamp()
                    self.UDPClientSocket.sendto(packet.packed_data_chunk_package(), self.serverAddressPort)

    def receive_ack(self):
        ack, address = self.UDPClientSocket.recvfrom(BUFFER_SIZE)
        ack = self.unpack_ack(ack)
        print("Received Ack:", ack)

        print("is_finished:", self.is_finished)
        if self.is_finished:
            return

        for w_packet in self.window:
            if w_packet.tag == ack:
                w_packet.change_state_as_Acked()
                break

        if self.window[0].get_state() == "acked":
            self.window.popleft()
            try:
                if self.data_chunk_list[self.last_appended_index]:
                    next_data_chunk = self.data_chunk_list[self.last_appended_index]
                    self.window.append(next_data_chunk)
                    self.last_appended_index += 1
            except IndexError:
                return

    def run(self):
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        interleaved_path_list = self.get_interleaved_path_list()

        self.split_data(interleaved_path_list)


        self.fill_the_window()

        while True:
            self.send_data()
            self.receive_ack()
            if self.is_finished:
                print("\nFinished sending all data chunks.")
                print("Remaining window length:", len(self.window))
                print("Last appended index:", self.last_appended_index)
                break

        self.UDPClientSocket.close()


          
udp_sr = UDP_with_Selective_Repeat()

udp_sr.run()
    


