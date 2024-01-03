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

# Dictionary to store message parts
message_parts = {}


    
def check_checksum(checksum, data):
    return checksum == hashlib.md5(data).digest()

def unpacked_data_chunk_package(packed_package):
        sequence_number, checksum, tag, chunk_length = struct.unpack(f'!I16sII', packed_package[:HEADER_SIZE])
        data_chunk = struct.unpack(f'{chunk_length}s', packed_package[HEADER_SIZE:HEADER_SIZE + chunk_length])[0]
        
        #if check_checksum(checksum, bytes(str(sequence_number), 'utf8') + \
        #    bytes(str(chunk_length), 'utf8') + data_chunk):
            
        return sequence_number, checksum, tag, chunk_length, data_chunk

def pack_ack(tag):
    return struct.pack('!I', tag)

while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    data = bytesAddressPair[0]
    address = bytesAddressPair[1]
    ack_list = []
    
    sequence_number, checksum, tag, chunk_length, data_chunk = unpacked_data_chunk_package(data)
    #if tag not in ack_list:
    #    ack_list.append(tag)

    ack = pack_ack(tag)
    UDPServerSocket.sendto(ack, address)
    
    # Here you need to parse the message to extract the sequence number and data
    # sequence_number, data = parse_message(message)
    
    # Save the data part using the sequence number as the key
    # message_parts[sequence_number] = data
    
    # Send an acknowledgement for the received message part
    # ack_message = create_ack(sequence_number)
    # UDPServerSocket.sendto(ack_message, address)

    # Once all parts are received, you can reconstruct the message
    # if check_all_parts_received(message_parts):
    #     full_message = reconstruct_message(message_parts)
    #     process_full_message(full_message)
    #     break  # or continue if you want to keep the server running
