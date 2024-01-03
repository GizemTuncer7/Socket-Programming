import os
import struct

# MACROS
BUFFER_SIZE = 1350
WINDOW_SIZE = 150

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