import datetime
import pickle
import struct
import hashlib
from helpers import TIMEOUT_INTERVAL

PACKAGE_SIZE = 1500         # 1500 bytes of data

SEQUENCE_NUMBER_SIZE = 4    # 4 bytes of sequence number

CHECKSUM_SIZE = 16          # 16 bytes of checksum

DATA_LENGTH_SIZE = 4        # 4 bytes of data length

TAG_LENGTH_SIZE = 4         # 4 bytes of tag length

HEADER_SIZE = SEQUENCE_NUMBER_SIZE + CHECKSUM_SIZE + DATA_LENGTH_SIZE + TAG_LENGTH_SIZE     # 28 bytes of header

DATA_CHUNK_SIZE = PACKAGE_SIZE - HEADER_SIZE    # 1472 bytes of data chunk


class Package:
    """
    Represents a single package of data in transmission.

    Attributes:
        packet_number (int): Unique identifier for the package.
        sequence_number (int): Sequence number to track ordering.
        tag (int): Tag identifying the type of package.
        data_chunk (bytes): Actual data contained in the package.
        current_state (str): Current state of the package (wait, sent, received, acked).
        sent_time (float): Timestamp when the package was sent.
        received_time (float): Timestamp when the package was received.

    """
    packet_number = 0
    sequence_number = 0
    tag = 0
    data_chunk = None
    package_header = None

    current_state = "wait"

    sent_time = None
    received_time = None

    def __init__(self, packet_number, sequence_number, tag, data_chunk=None):
        """
        Initialize a new package.

        Parameters:
        packet_number (int): Unique identifier for the package.
        sequence_number (int): File sequence number to track ordering.
        tag (int): Tag for each chunk/packet of the file.
        data_chunk (bytes): Actual data contained in the package.
        """
        self.packet_number = packet_number
        self.sequence_number = sequence_number % 100000
        self.data_chunk = data_chunk
        self.tag = tag
        self.sent_time = None
        self.received_time = None
    
    def get_state(self) -> str:
        """
        Returns the current state of the package.
        """
        return self.current_state
    
    def change_state_as_wait(self):
        self.current_state = "wait"
    
    def change_state_as_sent(self):
        """
        Changes the state of the package to sent and sets the sent time.
        """
        self.sent_time =datetime.datetime.utcnow().timestamp()
        self.current_state = "sent"
        return self

    def change_state_as_received(self, data):
        """
        Changes the state of the package to received and sets the received time.
        """
        self.data_chunk = data
        self.received_time = datetime.datetime.utcnow().timestamp()
        self.current_state = "received"
        return self
    
    def change_state_as_Acked(self):
        self.current_state = "acked"
        return self

    def get_checksum(self, data):
        """
        Calculates and returns the checksum of the given data.

        Parameters:
        data (bytes): The data to calculate the checksum of.

        Returns:
        bytes: The checksum of the given data.
        """
        return hashlib.md5(data).digest()
    
    def packed_data_chunk_package(self):
        """
        Packs the package into a single packet.

        Returns:
        bytes: The packed package. The package is packed as follows:
            - packet_number (int)
            - sequence_number (int)
            - checksum (bytes)
            - tag (int)
            - data_chunk_length (int)
            - data_chunk (bytes)
            - align_size (bytes)
        """
        data_chunk_length = len(self.data_chunk)

        checksum = self.get_checksum(bytes(str(self.packet_number), 'utf8') + \
            bytes(str(data_chunk_length), 'utf8') + self.data_chunk)
        
        # All packets must the same size, if the data chunk is smaller than the maximum size, we need to align it with spaces
        align_size = DATA_CHUNK_SIZE - data_chunk_length

        return struct.pack(f'!II16sII{data_chunk_length}s{align_size}s', self.packet_number, self.sequence_number, checksum, self.tag, data_chunk_length, self.data_chunk, b' ' * align_size)

    

    def is_timeout(self) -> bool:
        """
        Checks if the package has timed out by comparing the sent time with the current time.

        Returns:
        bool: True if the package has timed out, False otherwise.
        """
        return datetime.datetime.utcnow().timestamp() - self.sent_time >= TIMEOUT_INTERVAL
    
    def is_acked(self):
        return self.current_state == "acked"

    def __str__(self):
        return f'{self.packet_number}: {self.sequence_number} - {self.current_state}'
    




