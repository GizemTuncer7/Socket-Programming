import socket
import pickle 
import struct
import hashlib 

localIP = "server"
localPort = 8000
bufferSize = 1500

PACKAGE_SIZE = 1500

SEQUENCE_NUMBER_SIZE = 4

CHECKSUM_SIZE = 16

DATA_LENGTH_SIZE = 4

TAG_LENGTH_SIZE = 4

HEADER_SIZE = SEQUENCE_NUMBER_SIZE + CHECKSUM_SIZE + DATA_LENGTH_SIZE + TAG_LENGTH_SIZE 

DATA_CHUNK_SIZE = PACKAGE_SIZE - HEADER_SIZE

# Create a UDP socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

data_chunk_dict = {}


def check_checksum(checksum, data):
    return checksum == hashlib.md5(data).digest()

def unpacked_data_chunk_package(packed_package):
        sequence_number, checksum, tag, chunk_length = struct.unpack(f'!I16sII', packed_package[:HEADER_SIZE])
        data_chunk = struct.unpack(f'{chunk_length}s', packed_package[HEADER_SIZE:HEADER_SIZE + chunk_length])[0]
        
        #if check_checksum(checksum, bytes(str(sequence_number), 'utf8') + \
        #    bytes(str(chunk_length), 'utf8') + data_chunk):
            
        return sequence_number, checksum, tag, chunk_length, data_chunk

def pack_ack(sequence_number, tag):
    return struct.pack('!II', sequence_number, tag)

def send_ack(sequence_number, tag):
    ack = pack_ack(sequence_number, tag)
    UDPServerSocket.sendto(ack, address)

def receive_data(sequence_number, tag, data_chunk):
    if sequence_number in data_chunk_dict.keys():
        if tag not in data_chunk_dict[sequence_number].keys():
            data_chunk_dict[sequence_number][tag] = data_chunk
        else:
            print('duplicate')
    else:
        data_chunk_dict[sequence_number] = {tag: data_chunk}


while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    data = bytesAddressPair[0]
    address = bytesAddressPair[1]


    sequence_number, checksum, tag, chunk_length, data_chunk = unpacked_data_chunk_package(data)

    ack = pack_ack(sequence_number, tag)
    UDPServerSocket.sendto(ack, address)

    receive_data(sequence_number, tag, data_chunk)

    if sequence_number == 19 and tag == 740:
        break

file_list = []

for (seq_num, tag_chunk_dict) in data_chunk_dict.items():
    for (tag, chunk) in tag_chunk_dict.items():
        if (tag == None):
            print("ZOOOOOOOOOOOOORT")
        else:
        # print(f"\t Sequence Number: {seq_num} - Tag: {tag}")
            pass

        