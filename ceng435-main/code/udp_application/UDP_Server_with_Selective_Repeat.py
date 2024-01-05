import socket
import time
import pickle
import struct
import hashlib

from helpers import *


class UDP_Server_with_Selective_Repeat:
    """
    Represents a UDP server with selective repeat.

    Attributes:
        UDPServerSocket (socket): UDP socket used for transmission.
        data_chunk_dict (dict): Dictionary of data chunks for O(1) access.
        localIP (str): Local IP address.
        localPort (int): Local port number.
        bufferSize (int): Buffer size.
        address (tuple): Client address and port.
    """
    UDPServerSocket = None
    data_chunk_dict = None
    localIP = None
    localPort = None
    bufferSize = None
    address = None

    def __init__(self):
        self.data_chunk_dict = {}
        self.localIP = "server"
        self.localPort = 8000
        self.bufferSize = 1500
        self.address = None

    def send_ack(self, packet_number, sequence_number, tag):
        """
        Sends an acknowledgement to the client.

        Parameters:
            packet_number (int): Packet number.
            sequence_number (int): Sequence number (file number).
            tag (int): Tag (part number of the file).
        """
        ack = pack_ack(packet_number, sequence_number, tag)
        self.UDPServerSocket.sendto(ack, self.address)

    def listen_socket(self):
        """
        Listens the socket, receives data,
        Unpacks the data and sends an acknowledgement.
        """
        bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)
        received_data = bytesAddressPair[0]
        self.address = bytesAddressPair[1]

        packet_number, sequence_number, checksum, tag, chunk_length, data_chunk = unpacked_data_chunk_package(received_data)

        self.receive_data(sequence_number, tag, data_chunk)

        self.send_ack(packet_number, sequence_number, tag)


    def receive_data(self, sequence_number, tag, data_chunk):
        """
        Receives the data and stores it in the dictionary.
        Also checks if the data is present in the dictionary.

        Parameters:
            sequence_number (int): Sequence number (file number).
            tag (int): Tag (part number of the file).
            data_chunk (bytes): Data chunk.
        """
        if sequence_number in self.data_chunk_dict.keys():
            if tag not in self.data_chunk_dict[sequence_number].keys():
                self.data_chunk_dict[sequence_number][tag] = data_chunk
        else:
            self.data_chunk_dict[sequence_number] = {tag: data_chunk}

    def run(self):
        """
        Runs the server and receives the data from the client.
        """
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((self.localIP, self.localPort))

        while True:
            self.listen_socket()

            try:
                # This is a hardcoded part.
                # Since our window size is smaller then the a files packet number,
                # We can know if we received all the data by checking the dictionary size.
                if (self.data_chunk_dict.keys().__len__() == 20) and (self.data_chunk_dict[19].keys().__len__() == 741):
                    break
            except KeyError as e:
                print(e)
        