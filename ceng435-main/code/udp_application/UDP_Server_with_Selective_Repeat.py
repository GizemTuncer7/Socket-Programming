import socket
import time
import pickle
import struct
import hashlib

from helpers import *


class UDP_Server_with_Selective_Repeat:
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

    def send_ack(self, sequence_number, tag):
        ack = pack_ack(sequence_number, tag)
        self.UDPServerSocket.sendto(ack, self.address)

    def listen_socket(self):
        bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)
        received_data = bytesAddressPair[0]
        self.address = bytesAddressPair[1]

        sequence_number, checksum, tag, chunk_length, data_chunk = unpacked_data_chunk_package(received_data)

        self.receive_data(sequence_number, tag, data_chunk)

        self.send_ack(sequence_number, tag)



    def receive_data(self, sequence_number, tag, data_chunk):
        if sequence_number in self.data_chunk_dict.keys():
            if tag not in self.data_chunk_dict[sequence_number].keys():
                self.data_chunk_dict[sequence_number][tag] = data_chunk
            else:
                print("DUPLICATE")
                self.send_ack(sequence_number, tag)
        else:
            self.data_chunk_dict[sequence_number] = {tag: data_chunk}

    def run(self):
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((self.localIP, self.localPort))
        print("UDP server up and listening")

        while True:
            self.listen_socket()

            try:
                if (self.data_chunk_dict.keys().__len__() == 20) and (self.data_chunk_dict[19].keys().__len__() == 741):
                    print("DONE")
                    break
            except KeyError as e:
                print(e)
        