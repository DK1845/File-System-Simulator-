# disk.py

# Disk simulator: represents the memory blocks

disk_size = 50

disk = ['free'] * disk_size


def get_disk():
    return disk


def get_free_block_count():
    return disk.count('free')


def get_free_blocks():
    return [i for i, b in enumerate(disk) if b == 'free']


def allocate_contiguous(file_name, size):
    for i in range(disk_size - size + 1):
        if all(disk[i + j] == 'free' for j in range(size)):
            for j in range(size):
                disk[i + j] = file_name
            return list(range(i, i + size))
    return []


def allocate_linked(file_name, size):
    free = get_free_blocks()
    if len(free) >= size:
        for b in free[:size]:
            disk[b] = file_name
        return free[:size]
    return []


def allocate_indexed(file_name, size):
    free = get_free_blocks()
    if len(free) >= size + 1:
        index_block = free[0]
        data_blocks = free[1:size + 1]
        disk[index_block] = file_name
        for b in data_blocks:
            disk[b] = file_name
        return index_block, data_blocks
    return None, []


def free_blocks(file_name):
    for i in range(len(disk)):
        if disk[i] == file_name:
            disk[i] = 'free'