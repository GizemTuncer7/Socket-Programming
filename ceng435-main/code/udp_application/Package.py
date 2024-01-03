import datetime
import pickle
import struct
import hashlib


PACKAGE_SIZE = 1500

SEQUENCE_NUMBER_SIZE = 4

CHECKSUM_SIZE = 16

DATA_LENGTH_SIZE = 4

TAG_LENGTH_SIZE = 4

HEADER_SIZE = SEQUENCE_NUMBER_SIZE + CHECKSUM_SIZE + DATA_LENGTH_SIZE + TAG_LENGTH_SIZE 

DATA_CHUNK_SIZE = PACKAGE_SIZE - HEADER_SIZE


class Package:
    sequence_number = 0
    tag = 0
    data_chunk = None
    package_header = None

    current_state = "wait"

    sent_time = None
    received_time = None

    def __init__(self, sequence_number, tag, data_chunk=None):
        self.sequence_number = sequence_number % 100000
        self.data_chunk = data_chunk
        self.tag = tag
        self.sent_time = None
        self.received_time = None
    
    def get_state(self):
        return self.current_state
    
    def change_state_as_wait(self):
        self.current_state = "wait"
    
    def change_state_as_sent(self):
        self.sent_time =datetime.datetime.utcnow().timestamp()
        self.current_state = "sent"

    def change_state_as_received(self, data):
        self.data_chunk = data_chunk
        self.received_time = datetime.datetime.utcnow().timestamp()
        self.current_state = "received"
    
    def change_state_as_Acked(self):
        self.current_state = "acked"

    def get_checksum(self, data):
        return hashlib.md5(data).digest()
    
    def packed_data_chunk_package(self):
        data_chunk_length = len(self.data_chunk)

        checksum = self.get_checksum(bytes(str(self.sequence_number), 'utf8') + \
            bytes(str(data_chunk_length), 'utf8') + self.data_chunk)
        
        align_size = DATA_CHUNK_SIZE - data_chunk_length

        return struct.pack(f'!I16sII{data_chunk_length}s{align_size}s', self.sequence_number, checksum, self.tag, data_chunk_length, self.data_chunk, b' ' * align_size)

    

    def is_timeout(self):
        return datetime.datetime.utcnow().timestamp() - self.sent_time >= 20.0

    def __str__(self):
        return f'{self.sequence_number} - {self.current_state}'
    




