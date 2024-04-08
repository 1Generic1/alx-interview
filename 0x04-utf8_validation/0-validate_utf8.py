#!/usr/bin/python3
"""
    Determines if a given data set represents a valid UTF-8 encoding
"""


def validUTF8(data):
    """
    Determines if a given data set represents a valid UTF-8 encoding
    """
    num_bytes = 0

    for byte in data:
        # Check if the byte represents a continuation byte
        if num_bytes == 0:
            if byte >> 3 == 0b11110:
                num_bytes = 3
            elif byte >> 4 == 0b1110:
                num_bytes = 2
            elif byte >> 5 == 0b110:
                num_bytes = 1
            elif byte >> 7 == 0:
                num_bytes = 0
            else:
                return False
        else:
            if byte >> 6 != 0b10:
                return False
            num_bytes -= 1

    return num_bytes == 0
