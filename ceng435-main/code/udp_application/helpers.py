import hashlib
import os
import struct

# MACROS (client)
BUFFER_SIZE = 1350
WINDOW_SIZE = 150
TIMEOUT_INTERVAL = 0.001

# MACROS (server)
localIP = "server"
localPort = 8000
bufferSize = 1500

PACKAGE_SIZE = 1500

PACKET_NUMBER_SIZE = 4

SEQUENCE_NUMBER_SIZE = 4

CHECKSUM_SIZE = 16

DATA_LENGTH_SIZE = 4

TAG_LENGTH_SIZE = 4

HEADER_SIZE = PACKET_NUMBER_SIZE + SEQUENCE_NUMBER_SIZE + CHECKSUM_SIZE + DATA_LENGTH_SIZE + TAG_LENGTH_SIZE

DATA_CHUNK_SIZE = PACKAGE_SIZE - HEADER_SIZE


def interleave_parts(large_file_paths, small_file_paths) -> list:
    """
    interleaves the parts of the large and small files
    :param large_file_paths: list of paths to large files
    :param small_file_paths: list of paths to small files
    :return: interleaved list of paths
    """
    interleaved = []
    larger_list, smaller_list = (large_file_paths, small_file_paths) if len(large_file_paths) > len(
        small_file_paths) else (small_file_paths, large_file_paths)

    # Interleave parts from the larger and smaller lists
    for i in range(len(larger_list)):
        interleaved.append(larger_list[i])
        if i < len(smaller_list):
            interleaved.append(smaller_list[i])

    return interleaved


def get_interleaved_path_list() -> list:
    """
    returns the interleaved path list
    :return: interleaved path list
    """
    large_file_paths = []
    small_file_paths = []
    for i in range(10):                                                             # Reads 10 files
        large_file_paths.append(os.path.join('/root', 'objects', f"large-{i}.obj"))
        small_file_paths.append(os.path.join('/root', 'objects', f"small-{i}.obj"))

    interleaved_path_list = interleave_parts(large_file_paths, small_file_paths)
    return interleaved_path_list


def unpack_ack(packed_ack):
    """
    Unpack a packed acknowledgment (ack) into its constituent parts.

    Parameters:
    packed_ack (bytes): The packed ack received, expected to be a sequence of bytes.

    Returns:
    tuple[int, int, int]: A tuple containing three integers representing the packet number,
                          sequence number, and tag, respectively, extracted from the packed ack.
    """
    return struct.unpack('!III', packed_ack) 


def check_checksum(checksum, data) -> bool:
    """
    NOT USED

    Check if the checksum of the data is equal to the given checksum.

    Parameters:
    checksum (bytes): The checksum to check against.
    data (bytes): The data to check the checksum of.

    Returns:
    bool: True if the checksums are equal, False otherwise.

    """
    return checksum == hashlib.md5(data).digest()


def unpacked_data_chunk_package(packed_package):
    """
    Unpack a packed data chunk package into its constituent parts.

    Parameters:
    packed_package (bytes): The packed package received, expected to be a sequence of bytes.

    Returns:
    tuple[int, int, bytes, int, int, bytes]: A tuple containing the packet number, sequence number,
                                           checksum, tag, chunk length, and data chunk, respectively,
                                           extracted from the packed package.
    """
    packet_number, sequence_number, checksum, tag, chunk_length = struct.unpack(f'!II16sII', packed_package[:HEADER_SIZE])
    data_chunk = struct.unpack(f'{chunk_length}s', packed_package[HEADER_SIZE:HEADER_SIZE + chunk_length])[0]

    # if check_checksum(checksum, bytes(str(sequence_number), 'utf8') + \
    #    bytes(str(chunk_length), 'utf8') + data_chunk):

    return packet_number, sequence_number, checksum, tag, chunk_length, data_chunk


def pack_ack(packet_number, sequence_number, tag) -> bytes:
    """
    Pack the given packet number, sequence number, and tag into a single packet.

    Parameters:
    packet_number (int): The packet number to pack.
    sequence_number (int): The sequence number to pack.
    tag (int): The tag to pack.

    Returns:
    bytes: The ACK packet containing the packet number, sequence number, and tag.
    """
    return struct.pack('!III', packet_number, sequence_number, tag)
