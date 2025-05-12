# file_manager.py

import os
from storage import save_state, load_state

# Disk simulator and file directory
disk_size = 50
disk = ['free'] * disk_size
file_directory = {}

# Load previously saved state, if any
saved_data = load_state()
if saved_data:
    disk = saved_data["disk"]
    file_directory = saved_data["file_directory"]

# Utility functions
def get_disk():
    return disk

def get_free_block_count():
    return disk.count('free')

def get_free_blocks():
    return [i for i, b in enumerate(disk) if b == 'free']

# Disk Allocation Methods
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

# Core File Operations
def create_file(file_name, file_size, allocation_method, file_type, file_data):
    if file_name in file_directory:
        return False  # File already exists

    blocks = []
    index_block = None

    if allocation_method == 'Contiguous':
        blocks = allocate_contiguous(file_name, file_size)
    elif allocation_method == 'Linked':
        blocks = allocate_linked(file_name, file_size)
    elif allocation_method == 'Indexed':
        index_block, data_blocks = allocate_indexed(file_name, file_size)
        if index_block is not None:
            blocks = data_blocks

    if not blocks:
        return False  # Allocation failed

    file_directory[file_name] = {
        'size': file_size,
        'method': allocation_method,
        'blocks': blocks,
        'type': file_type,
        'content': file_data,
        'index': index_block if allocation_method == 'Indexed' else None
    }

    save_state({"disk": disk, "file_directory": file_directory})
    return True

def delete_file(file_name):
    if file_name in file_directory:
        for block in file_directory[file_name]['blocks']:
            disk[block] = 'free'
        if file_directory[file_name]['method'] == 'Indexed':
            index_block = file_directory[file_name].get('index')
            if index_block is not None:
                disk[index_block] = 'free'
        del file_directory[file_name]
        save_state({"disk": disk, "file_directory": file_directory})

def get_all_files():
    return file_directory

def get_file_content(file_name):
    if file_name in file_directory:
        return file_directory[file_name]['content']
    return None

def update_file_content(file_name, new_content):
    if file_name in file_directory:
        file_directory[file_name]['content'] = new_content
        save_state({"disk": disk, "file_directory": file_directory})
        return True
    return False
