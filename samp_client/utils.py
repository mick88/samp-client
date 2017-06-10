from __future__ import unicode_literals, absolute_import


def encode_bytes(*args):
    """
    Encodes values into a byte string
    strings are left as-is
    integer values are encoded into their char values
    :return: bytestring representing all arguments joined together
    """
    result = b''
    for arg in args:
        if isinstance(arg, basestring):
            result += str(arg)
        elif isinstance(arg, int):
            result += chr(arg)
    return result


def decode_int(string):
    """
    Decodes integer from byte string
    """
    result = 0
    for n, c in enumerate(string):
        result |= ord(c) << (8 * n)
    return result


def decode_string(string, len_pos, len_bytes=4):
    """
    Decodes string from a string
    :param string: bytestring with the response
    :param len_pos: position of the integer expressing the length
    :param len_bytes: number of bytes used for string length
    :return: substring of string starting at len_pos + len_bytes and ending at position indicated in length value at position len_pos
    """
    assert isinstance(len_pos, int)
    len_end = len_pos + len_bytes
    length = decode_int(string[len_pos:len_end])
    return string[len_end:len_end + length]
