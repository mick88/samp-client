from __future__ import unicode_literals, absolute_import

import re
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


def build_rcon_command(command, args=None):
    """
    Appends args to the command
    :param command: the command string
    :param args: list of arguments or a single argument (bool, string or int)
    """
    if args is not None:
        # Bool check must come first because bool extends int
        if isinstance(args, bool):
            args = int(args),
        elif isinstance(args, (basestring, int, float)):
            args = args,
        if len(args):
            command += ' ' + ' '.join(str(arg) for arg in args)
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