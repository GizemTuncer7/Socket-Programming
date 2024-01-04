import socket
from collections import deque
import Package
import datetime
import Package
import time

from helpers import *

class UDP_Client_with_Selective_Repeat:
    data_chunk_list = None
    last_appended_index = None
    is_finished = None
    serverAddressPort = None
    UDPClientSocket = None

    def __init__(self):
        self.window = deque(maxlen=WINDOW_SIZE)
        self.data_chunk_list = []
        self.last_appended_index = 0
        self.is_finished = False
        self.serverAddressPort = ("server", 8000)
        self.UDPClientSocket = None

    def split_data(self, interleaved_path_list):
        sequence_number = 0
        for interleaved_path in interleaved_path_list:
            with open(interleaved_path, 'rb') as file:
                tag = 0
                while True:
                    data_chunk = file.read(BUFFER_SIZE)
                    if not data_chunk:
                        break
                    packet = Package.Package(sequence_number=sequence_number, data_chunk=data_chunk, tag=tag)
                    tag += 1
                    self.data_chunk_list.append(packet)
                sequence_number += 1

    def fill_the_window(self):
        while len(self.window) < WINDOW_SIZE:
            try:
                packet = self.data_chunk_list[self.last_appended_index]
                self.window.append(packet)
                self.last_appended_index += 1
            except StopIteration:
                break

    def send_data(self):
        # print("Send Data Window Length:", len(self.window))
        for packet in self.window:
            if packet.get_state() == "wait":
                packet.change_state_as_sent()
                # print(f"Sending packet with sequence number {packet.sequence_number} and tag {packet.tag}")
                packed_package = packet.packed_data_chunk_package()
                self.UDPClientSocket.sendto(packed_package, self.serverAddressPort)
            elif packet.get_state() == "sent":
                if packet.is_timeout():
                    # print(f"Timeout, sequence number = {packet.sequence_number} {packet.tag}")
                    packet.sent_time = datetime.datetime.utcnow().timestamp()
                    self.UDPClientSocket.sendto(packet.packed_data_chunk_package(), self.serverAddressPort)



    def receive_ack(self):
        ack, address = self.UDPClientSocket.recvfrom(BUFFER_SIZE)

        if (ack == None):
            raise Exception("Ack is None")

        sequence_number, tag = unpack_ack(ack)
        # print(f"Received Ack: {sequence_number} - {tag}")

        # print("Receive Ack Window Length:", len(self.window))
        if len(self.window) == 0:
            # print("Window is empty")
            self.is_finished = True
            return

        for w_packet in self.window:
            if w_packet.sequence_number == sequence_number and w_packet.tag == tag:
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
                pass

        if len(self.window) == 0:
            # print("Window is empty")
            self.is_finished = True


    def run(self):
        now = time.time()

        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        interleaved_path_list = get_interleaved_path_list()

        self.split_data(interleaved_path_list)

        self.fill_the_window()

        while True:
            self.send_data()
            self.receive_ack()

            if self.is_finished:
                break

        self.UDPClientSocket.close()

        end = time.time()

        # elapsed time in seconds
        elapsed = end - now
        print(f"Elapsed time: {elapsed} seconds on UDP {socket.gethostname()}")
