import socket
from collections import deque
import Package
import datetime
import time

from helpers import *

class UDP_Client_with_Selective_Repeat:
    packets = None
    last_appended_index = None
    is_finished = None
    serverAddressPort = None
    UDPClientSocket = None
    packets_length = None
    send_base = 0
    next_sequence_number = 0

    def __init__(self):
        self.send_base = 0
        self.next_sequence_number = 0
        self.packets_length = 0
        self.packets = deque()
        
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
                    packet = Package.Package(packet_number=self.packets_length, sequence_number=sequence_number, data_chunk=data_chunk, tag=tag)
                    tag += 1
                    self.packets_length += 1
                    self.packets.append(packet)
                sequence_number += 1


    def send_data(self):
        # print("Send Data Window Length:", len(self.window))
        if  self.next_sequence_number < self.packets_length and (self.next_sequence_number - self.send_base) < WINDOW_SIZE:
            # print("next_sequence_number:", self.next_sequence_number)
            self.packets[self.next_sequence_number].change_state_as_sent()
            self.UDPClientSocket.sendto(self.packets[self.next_sequence_number].packed_data_chunk_package(), self.serverAddressPort)
            self.next_sequence_number += 1

        if self.send_base < self.packets_length and self.packets[self.send_base].is_timeout():
            self.packets[self.send_base].change_state_as_sent()
            self.UDPClientSocket.sendto(self.packets[self.send_base].packed_data_chunk_package(), self.serverAddressPort)


    def receive_ack(self):
        try:
            ack, address = self.UDPClientSocket.recvfrom(BUFFER_SIZE)
        except:
            return

        packet_number, sequence_number, tag = unpack_ack(ack)
        # print(f"Received Ack: {sequence_number} - {tag}")

        # print("Receive Ack Window Length:", len(self.window))

        self.packets[packet_number] = self.packets[packet_number].change_state_as_Acked()

        if packet_number == self.send_base:
            self.send_base += 1
            if (self.send_base == self.packets_length):
                self.is_finished = True

         

    def run(self):
        now = time.time()

        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPClientSocket.setblocking(0)

        interleaved_path_list = get_interleaved_path_list()

        self.split_data(interleaved_path_list)

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
