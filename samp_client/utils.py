import re

from samp_client.constants import ENCODING
from samp_client.models import ServerVar

VAR_PATTERN = re.compile(r'\s*'.join((
    r'(?P<name>\w+)',
    r'=',
    r'(?P<value>.+?)',
    r'\((?P<type>string|int|bool|float)\)',
    r'(?P<read_only>\(read-only\))?',
)))

VAR_TYPES = {
    'int': int,
    'bool': bool,
    'string': str,
    'float': float,
}


def encode_bytes(*args):
    """
    Encodes values into a byte string
    bytestrings are left as-is
    integer values are encoded into their char values
    :return: bytestring representing all arguments joined together
    """
    result = b''
    for arg in args:
        if isinstance(arg, bytes):
            result += arg
        elif isinstance(arg, str):
            result += bytes(arg, ENCODING)
        elif isinstance(arg, int):
            result += bytes([arg])
    return result


def decode_int(data):
    """ Decodes integer from byte string """
    assert isinstance(data, bytes)
    return sum(c << (8 * n) for n, c in enumerate(data))


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
    return string[len_end:len_end + length].decode(ENCODING)


def build_rcon_command(command, args=None):
    """
    Appends args to the command
    :param command: the command string
    :param args: list of arguments or a single argument (bool, string or int)
    """
    if isinstance(command, str):
        command = command.encode(ENCODING)
    if args is not None:
        # Bool check must come first because bool extends int
        if isinstance(args, bool):
            args = int(args),
        elif isinstance(args, (str, bytes, int, float)):
            args = args,
        if len(args):
            args = map(str, args)
            command += b' ' + b' '.join(bytes(arg, ENCODING) for arg in args)
    return command


def parse_server_var(variable):
    """ Parses server variable string into a ServerVar named tuple"""
    matches = VAR_PATTERN.match(variable)
    if matches:
        groups = matches.groupdict()
        val_type = VAR_TYPES[groups['type']]
        # Strip surrounding whitespace and quotations from value
        value = groups['value']
        if val_type == bool:
            # pre-parse boolean to int as it will be returned as 0 or 1 string
            value = int(value)
        elif val_type == str:
            # strip surrounding quotations from string value
            value = value.strip('"')
        return ServerVar(
            name=groups['name'],
            value=val_type(value),
            read_only=bool(groups['read_only']),
        )
    else:
        raise ValueError('Failed to parse {}'.format(variable))