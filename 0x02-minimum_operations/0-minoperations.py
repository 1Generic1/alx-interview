#!/usr/bin/python3
"""
    Calculate the fewest number of operations needed to
    result in exactly n 'H' characters in the file.
"""


def minOperations(n):
    """
    Calculate the fewest number of operations needed to
    result in exactly n 'H' characters in the file.
    """
    if n == 1:
        return 0

    operations = 0
    paste_buffer = 1
    clipboard = 1

    while paste_buffer < n:
        if n % paste_buffer == 0:
            clipboard = paste_buffer
            operations += 1
        paste_buffer += clipboard
        operations += 1
    return operations
