import socket
from collections import deque
import Package
import datetime
import time

from helpers import *

class UDP_Client_with_Selective_Repeat:
    """
    Represents a UDP client with selective repeat.

    Attributes:
        packets (deque): List of packets to be sent.
        last_appended_index (int): Last index of the list of packets.
        is_finished (bool): Indicates whether the transmission is finished.
        serverAddressPort (tuple): Server address and port.
        UDPClientSocket (socket): UDP socket used for transmission.
        packets_length (int): Length of the list of packets.
        send_base (int): Send base of the window.
        next_sequence_number (int): Next (next to be sent) sequence number of the window.
    """
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
        """
        Splits the data into packets and appends them to the list of packets.
        With their packet number, sequence number, tag and data chunk.

        Parameters:
        interleaved_path_list (list): List of paths of interleaved files.
        """
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
        """
        Sends a available packet from the window
        """
        # if next sequence number is in the packet list and in the window send that packet and increase next sequence number
        if self.next_sequence_number < self.packets_length and (self.next_sequence_number - self.send_base) < WINDOW_SIZE:
            self.packets[self.next_sequence_number].change_state_as_sent()
            self.UDPClientSocket.sendto(self.packets[self.next_sequence_number].packed_data_chunk_package(), self.serverAddressPort)
            self.next_sequence_number += 1

        # if send base is in the packet list and it is timeout send that packet
        if self.send_base < self.packets_length:
            if self.packets[self.send_base].is_timeout():
                self.packets[self.send_base].change_state_as_sent()
                self.UDPClientSocket.sendto(self.packets[self.send_base].packed_data_chunk_package(), self.serverAddressPort)


    def receive_ack(self):
        """
        Receives ack from the server and updates the window
        """
        try:
            # If there are BUFFER_SIZE bytes of data available, it is returned as a bytes object. Otherwise, don't block.
            ack, address = self.UDPClientSocket.recvfrom(BUFFER_SIZE)
        except BlockingIOError:
            # Check if the send base is acked, if it is acked increase send base
            if self.packets[self.send_base].is_acked():
                self.send_base += 1
                if (self.send_base == self.packets_length):
                    # if send base is equal to packet length then transmission is finished
                    self.is_finished = True
            return

        packet_number, sequence_number, tag = unpack_ack(ack)   # unpack ack to get packet number, sequence number and tag

        self.packets[packet_number] = self.packets[packet_number].change_state_as_Acked() # change packet state as acked

        # if packet number is equal to send base or send base is acked increase send base
        if packet_number == self.send_base or self.packets[self.send_base].is_acked():
            self.send_base += 1
            if (self.send_base == self.packets_length):
                self.is_finished = True

         

    def run(self):
        """
        Runs the client and sends the data to the server.
        """
        now = time.time()

        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPClientSocket.setblocking(0) # Don't block when receiving data, if there is no data available, raise an error

        interleaved_path_list = get_interleaved_path_list()

        self.split_data(interleaved_path_list)

        while True:
            self.send_data()    # Checks if there is a packet to be sent and sends it
            self.receive_ack()  # Checks if there is an ack to be received and receives it

            if self.is_finished:
                break

        self.UDPClientSocket.close()

        end = time.time()

        # elapsed time in seconds
        elapsed = end - now
        print(f"{elapsed}")
