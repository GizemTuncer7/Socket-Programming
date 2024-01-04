import hashlib
import os
import struct

# MACROS (client)
BUFFER_SIZE = 1350
WINDOW_SIZE = 150

# MACROS (server)
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


def interleave_parts(large_file_paths, small_file_paths):
    interleaved = []
    larger_list, smaller_list = (large_file_paths, small_file_paths) if len(large_file_paths) > len(
        small_file_paths) else (small_file_paths, large_file_paths)

    # Interleave parts from the larger and smaller lists
    for i in range(len(larger_list)):
        interleaved.append(larger_list[i])
        if i < len(smaller_list):
            interleaved.append(smaller_list[i])

    return interleaved


def get_interleaved_path_list():
    large_file_paths = []
    small_file_paths = []
    for i in range(10):
        large_file_paths.append(os.path.join('/root', 'objects', f"large-{i}.obj"))
        small_file_paths.append(os.path.join('/root', 'objects', f"small-{i}.obj"))

    interleaved_path_list = interleave_parts(large_file_paths, small_file_paths)
    return interleaved_path_list


def unpack_ack(packed_ack):
    return struct.unpack('!II', packed_ack)


def check_checksum(checksum, data):
    return checksum == hashlib.md5(data).digest()


def unpacked_data_chunk_package(packed_package):
    sequence_number, checksum, tag, chunk_length = struct.unpack(f'!I16sII', packed_package[:HEADER_SIZE])
    data_chunk = struct.unpack(f'{chunk_length}s', packed_package[HEADER_SIZE:HEADER_SIZE + chunk_length])[0]

    # if check_checksum(checksum, bytes(str(sequence_number), 'utf8') + \
    #    bytes(str(chunk_length), 'utf8') + data_chunk):

    return sequence_number, checksum, tag, chunk_length, data_chunk


def pack_ack(sequence_number, tag):
    return struct.pack('!II', sequence_number, tag)
