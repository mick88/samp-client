from __future__ import unicode_literals, absolute_import

import socket

from samp_client.constants import *
from samp_client.models import ServerInfo, Rule
from samp_client.utils import encode_bytes, decode_int, decode_string


class SampClient(object):
    """
    Client class for communicating with SA-MP Query API
    http://wiki.sa-mp.com/wiki/Query_Mechanism
    """

    def __init__(self, address='127.0.0.1', port=7777):
        super(SampClient, self).__init__()
        assert isinstance(port, int)
        assert isinstance(address, basestring)
        self.address = address
        self.port = port

    def connect(self):
        self.address = socket.gethostbyname(self.address)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return self

    def disconnect(self):
        self.socket.close()
        del self.socket

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'socket'):
            self.disconnect()

    def send_request(self, opcode):
        body = b'SAMP{ip}{port}{opcode}'.format(
            ip=encode_bytes(*[(int(n)) for n in self.address.split('.')]),
            port=encode_bytes(self.port & 0xFF, self.port >> 8 & 0xFF),
            opcode=opcode,
        )
        self.socket.sendto(body, (self.address, self.port))

        response = self.socket.recv(4096)
        # Strip header from the response
        return response[11:]

    def get_server_info(self):
        response = self.send_request(OPCODE_INFO)

        offset = 0
        hostname = decode_string(response, 5, 4)
        offset += len(hostname)
        gamemode = decode_string(response, offset + 9, 4)
        offset += len(gamemode)
        language = decode_string(response, offset + 13, 4)

        return ServerInfo(
            password=bool(response[0]),
            players=decode_int(response[1:3]),
            max_players=decode_int(response[3:5]),
            hostname=hostname,
            gamemode=gamemode,
            language=language,
        )

    def get_server_rules(self):
        response = self.send_request(OPCODE_RULES)
        num_rules = decode_int(response[:2])
        offset = 2
        for n in xrange(num_rules):
            name = decode_string(response, offset, len_bytes=1)
            offset += 1 + len(name)
            value = decode_string(response, offset, len_bytes=1)
            offset += 1 + len(value)
            yield Rule(
                name=name,
                value=value,
            )

    def get_server_rules_dict(self):
        return {rule.name: rule.value for rule in self.get_server_rules()}