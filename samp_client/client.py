from __future__ import unicode_literals, absolute_import

import socket

from samp_client.constants import *
from samp_client.models import ServerInfo, Rule, Client, ClientDetail
from samp_client.utils import encode_bytes, decode_int, decode_string


class SampClient(object):
    """
    Client class for communicating with SA-MP Query API
    http://wiki.sa-mp.com/wiki/Query_Mechanism
    """
    timeout = 1.0

    def __init__(self, address='127.0.0.1', port=7777, rcon_password=None):
        super(SampClient, self).__init__()
        assert isinstance(port, int)
        assert isinstance(address, basestring)
        self.address = address
        self.port = port
        self.rcon_password = rcon_password

    def connect(self):
        self.address = socket.gethostbyname(self.address)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(self.timeout)
        return self

    def disconnect(self):
        self.socket.close()
        del self.socket

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'socket'):
            self.disconnect()

    def send_request(self, opcode, extras=None, return_response=True):
        body = b'SAMP{ip}{port}{opcode}{extras}'.format(
            ip=encode_bytes(*[(int(n)) for n in self.address.split('.')]),
            port=encode_bytes(self.port & 0xFF, self.port >> 8 & 0xFF),
            opcode=opcode,
            extras=extras or '',
        )
        self.socket.sendto(body, (self.address, self.port))

        if return_response:
            return self.receive()

    def receive(self, buffersize=4096, strip_header=True):
        try:
            response = self.socket.recv(buffersize)
            # Strip header from the response
            return response[11:] if strip_header else response
        except socket.timeout as e:
            pass

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

    def get_server_clients(self):
        response = self.send_request(OPCODE_CLIENTS)
        num_clients = decode_int(response[:2])
        offset = 2
        for n in xrange(num_clients):
            name = decode_string(response, offset, len_bytes=1)
            offset += 1 + len(name)
            score = decode_int(response[offset:offset + 4])
            offset += 4
            yield Client(
                name=name,
                score=score,
            )

    def get_server_clients_detailed(self):
        response = self.send_request(OPCODE_CLIENTS_DETAILED)
        num_clients = decode_int(response[:2])
        offset = 2
        for n in xrange(num_clients):
            player_id = decode_int(response[offset])
            offset += 1
            name = decode_string(response, offset, len_bytes=1)
            offset += 1 + len(name)
            score = decode_int(response[offset:offset + 4])
            offset += 4
            ping = decode_int(response[offset:offset + 4])
            offset += 4
            yield ClientDetail(
                id=player_id,
                name=name,
                score=score,
                ping=ping,
            )

    def probe_server(self, value='ping'):
        assert len(value) == 4, 'Value must be exactly 4 characters'
        response = self.send_request(OPCODE_PSEUDORANDOM, extras=value)
        return response

    def validate_server(self, value='ping'):
        """
        Sends a query to server and validates that response matches the requested value
        """
        response = self.probe_server(value)
        if response != value:
            raise ValueError('Server returned {} instead of {}'.format(response, value))

    def send_rcon_command(self, command):
        if not self.rcon_password:
            raise ValueError('Rcon password was not provided')
        pass_len = len(self.rcon_password)
        command_len = len(command)
        rcon_payload = '{password_length}{password}{command_length}{command}'.format(
            password_length=encode_bytes(pass_len & 0xFF, pass_len >> 8 & 0xFF),
            password=self.rcon_password,
            command_length=encode_bytes(command_len & 0xFF, command_len >> 8 & 0xFF),
            command=command,
        )
        self.send_request(OPCODE_RCON, extras=rcon_payload, return_response=False)
        while True:
            next_line = self.receive()
            if next_line:
                yield decode_string(next_line, 0, 2)
            else:
                break