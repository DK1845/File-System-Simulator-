# file_manager.py

import os

# Disk simulator: represents the memory blocks
disk_size = 50
disk = ['free'] * disk_size
file_directory = {}  # To store file metadata

# Function to get current disk state
def get_disk():
    return disk

# Function to get free block count
def get_free_block_count():
    return disk.count('free')

# Function to get list of free blocks
def get_free_blocks():
    return [i for i, b in enumerate(disk) if b == 'free']

# Function to create a new file
def create_file(file_name, file_size, allocation_method, file_type, file_data):
    # Check if the file already exists
    if file_name in file_directory:
        return False  # File already exists

    # Allocate space for the file
    blocks = []
    if allocation_method == 'Contiguous':
        blocks = allocate_contiguous(file_name, file_size)
    elif allocation_method == 'Linked':
        blocks = allocate_linked(file_name, file_size)
    elif allocation_method == 'Indexed':
        index_block, data_blocks = allocate_indexed(file_name, file_size)
        if index_block:
            blocks = data_blocks

    if not blocks:
        return False  # No available space or failed allocation

    # Store file information in the file directory
    file_directory[file_name] = {
        'size': file_size,
        'method': allocation_method,
        'blocks': blocks,
        'type': file_type,
        'content': file_data,
        'index': index_block if allocation_method == 'Indexed' else None
    }
    return True

# Function to delete a file
def delete_file(file_name):
    if file_name in file_directory:
        # Free the allocated blocks
        for block in file_directory[file_name]['blocks']:
            disk[block] = 'free'
        del file_directory[file_name]

# Function to get all files and their information
def get_all_files():
    return file_directory

# Function to get the content of a file
def get_file_content(file_name):
    if file_name in file_directory:
        return file_directory[file_name]['content']
    return None

# Function to update the content of a file
def update_file_content(file_name, new_content):
    if file_name in file_directory:
        file_directory[file_name]['content'] = new_content
        return True
    return False

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
