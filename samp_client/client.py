from __future__ import unicode_literals, absolute_import

import socket

from samp_client.constants import *
from samp_client.exceptions import SampError, RconError, InvalidRconPassword
from samp_client.models import ServerInfo, Rule, Client, ClientDetail, RConPlayer
from samp_client.utils import encode_bytes, decode_int, decode_string, build_rcon_command, parse_server_var


class SampClient(object):
    """
    Client class for communicating with SA-MP Query API
    http://wiki.sa-mp.com/wiki/Query_Mechanism
    """
    timeout = 1.0

    def __init__(self, address='127.0.0.1', port=7777, rcon_password=None):
        super(SampClient, self).__init__()
        assert isinstance(address, basestring)
        self.address = address
        self.port = int(port)
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
        result = []
        for n in xrange(num_rules):
            name = decode_string(response, offset, len_bytes=1)
            offset += 1 + len(name)
            value = decode_string(response, offset, len_bytes=1)
            offset += 1 + len(value)
            rule = Rule(
                name=name,
                value=value,
            )
            result.append(rule)
        return result

    def get_server_rules_dict(self):
        return {rule.name: rule.value for rule in self.get_server_rules()}

    def get_server_clients(self):
        response = self.send_request(OPCODE_CLIENTS)
        num_clients = decode_int(response[:2])
        offset = 2
        result = []
        for n in xrange(num_clients):
            name = decode_string(response, offset, len_bytes=1)
            offset += 1 + len(name)
            score = decode_int(response[offset:offset + 4])
            offset += 4
            client = Client(
                name=name,
                score=score,
            )
            result.append(client)
        return result

    def get_server_clients_detailed(self):
        response = self.send_request(OPCODE_CLIENTS_DETAILED)
        num_clients = decode_int(response[:2])
        offset = 2
        result = []
        for n in xrange(num_clients):
            player_id = decode_int(response[offset])
            offset += 1
            name = decode_string(response, offset, len_bytes=1)
            offset += 1 + len(name)
            score = decode_int(response[offset:offset + 4])
            offset += 4
            ping = decode_int(response[offset:offset + 4])
            offset += 4
            detail = ClientDetail(
                id=player_id,
                name=name,
                score=score,
                ping=ping,
            )
            result.append(detail)
        return result

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
            raise SampError('Server returned {} instead of {}'.format(response, value))

    @property
    def rcon_password_bytes(self):
        """
        password prefixed with its encoded length
        """
        if not self.rcon_password:
            raise RconError('Rcon password was not provided')
        pass_len = len(self.rcon_password)
        return encode_bytes(pass_len & 0xFF, pass_len >> 8 & 0xFF) + self.rcon_password

    def send_rcon_command(self, command, args=tuple(), fetch_response=True):
        """
        Send any command to the server
        leading whitespace is stripped from the response
        :param command: the comand to send
        :param args: tuple or list of arguments to be appended to the command. Can be also a string or an int if only one argument is expected.
        :param fetch_response: Whether to receive response from server. Set this to False if you're not expecting a response; WARNING: If there is a response and you don't fetch it, it may be output as a response of your next command.
        :return list of lines responded from the server or None if fetch_response == False
        """
        command = build_rcon_command(command, args)
        command_len = len(command)
        rcon_payload = '{password}{command_length}{command}'.format(
            password=self.rcon_password_bytes,
            command_length=encode_bytes(command_len & 0xFF, command_len >> 8 & 0xFF),
            command=command,
        )
        self.send_request(OPCODE_RCON, extras=rcon_payload, return_response=False)
        if fetch_response:
            result = []
            while True:
                response = self.receive()
                if response is None:
                    break
                line = decode_string(response, 0, 2)
                if line:
                    result.append(line.lstrip())
                else:
                    break
        if len(result) == 1 and result[0] == 'Invalid RCON password.':
            raise InvalidRconPassword
        return result

    def rcon_cmdlist(self):
        """ List of rcon commands """
        return self.send_rcon_command(RCON_CMDLIST)[1:]

    def rcon_varlist(self):
        """ List of server variables """
        vars = self.send_rcon_command(RCON_VARLIST)[1:]
        return [parse_server_var(var) for var in vars]

    def rcon_varlist_dict(self):
        """ Server vars as a dictionary mapping variable name to its value """
        return {var.name: var.value for var in self.rcon_varlist()}

    def rcon_exit(self):
        return self.send_rcon_command(RCON_EXIT, fetch_response=False)

    def rcon_echo(self, text):
        """ Print message to server console and send it back as a string"""
        return self.send_rcon_command(RCON_ECHO, args=(text,))[0]

    def rcon_set_hostname(self, name):
        return self.send_rcon_command(RCON_HOSTNAME, args=(name,), fetch_response=False)

    def rcon_get_hostname(self):
        response = self.send_rcon_command(RCON_HOSTNAME)[0]
        return parse_server_var(response)

    def rcon_set_gamemodetext(self, name):
        return self.send_rcon_command(RCON_GAMEMODETEXT, args=(name,), fetch_response=False)

    def rcon_get_gamemodetext(self):
        response = self.send_rcon_command(RCON_GAMEMODETEXT)[0]
        return parse_server_var(response)

    def rcon_set_mapname(self, name):
        return self.send_rcon_command(RCON_MAPNAME, args=(name,), fetch_response=False)

    def rcon_get_mapname(self):
        response = self.send_rcon_command(RCON_MAPNAME)[0]
        return parse_server_var(response)

    def rcon_exec(self, filename):
        response = self.send_rcon_command(RCON_EXEC, args=(filename,))
        if len(response) == 1:
            # Error response is returned as a single string
            raise SampError(response[0])
        else:
            return response

    def rcon_kick(self, player_id):
        return self.send_rcon_command(RCON_KICK, args=(player_id,))

    def rcon_ban(self, player_id):
        return self.send_rcon_command(RCON_BAN, args=(player_id,))

    def rcon_banip(self, ip_address):
        return self.send_rcon_command(RCON_BANIP, args=(ip_address,))

    def rcon_unbanip(self, ip_address):
        return self.send_rcon_command(RCON_UNBANIP, args=(ip_address,))

    def rcon_changemode(self, mode):
        return self.send_rcon_command(RCON_CHANGEMODE, args=(mode,))

    def rcon_gmx(self):
        return self.send_rcon_command(RCON_GMX)

    def rcon_reloadbans(self):
        return self.send_rcon_command(RCON_RELOADBANS)

    def rcon_reloadlog(self):
        return self.send_rcon_command(RCON_RELOADBANS)

    def rcon_say(self, message):
        return self.send_rcon_command(RCON_SAY, args=(message,))

    def rcon_players(self):
        result = []
        for line in self.send_rcon_command(RCON_PLAYERS)[1:]:
            player_id, name, ping, ip = line.split('\t')
            player = RConPlayer(
                id=int(player_id),
                name=str(name),
                ping=int(ping),
                ip=str(ip),
            )
            result.append(player)
        return result

    def rcon_gravity(self, gravity=0.008):
        return self.send_rcon_command(RCON_GRAVITY, args=(gravity,))

    def rcon_weather(self, weather):
        return self.send_rcon_command(RCON_WEATHER, args=(weather,))

    def rcon_loadfs(self, name):
        response = self.send_rcon_command(RCON_LOADFS, args=(name,))[0]
        if 'load failed' in response:
            raise SampError(response)
        else:
            return response

    def rcon_unloadfs(self, name):
        response = self.send_rcon_command(RCON_UNLOADFS, args=(name,))[0]
        if 'unload failed' in response:
            raise SampError(response)
        else:
            return response

    def rcon_reloadfs(self, name):
        response = self.send_rcon_command(RCON_RELOADFS, args=(name,))
        if 'load failed' in response[-1]:
            raise SampError(response[-1])
        else:
            return response

    def rcon_get_weburl(self):
        response = self.send_rcon_command(RCON_WEBURL)[0]
        return parse_server_var(response)

    def rcon_set_weburl(self, url):
        return self.send_rcon_command(RCON_WEBURL, args=(url,))

    def rcon_set_rcon_password(self, password):
        """
        Set server's rcon password
        local password will be updated for future rcon commands
        """
        result = self.send_rcon_command(RCON_RCON_PASSWORD, args=(password,))
        self.rcon_password = password

    def rcon_get_rcon_password(self):
        response = self.send_rcon_command(RCON_RCON_PASSWORD)[0]
        return parse_server_var(response)

    def rcon_get_password(self):
        response = self.send_rcon_command(RCON_PASSWORD)[0]
        return parse_server_var(response)

    def rcon_set_password(self, password):
        return self.send_rcon_command(RCON_PASSWORD, args=(password,))[0]

    def rcon_get_messageslimit(self):
        response = self.send_rcon_command(RCON_MESSAGESLIMIT)[0]
        return parse_server_var(response)

    def rcon_set_messageslimit(self, limit):
        return self.send_rcon_command(RCON_MESSAGESLIMIT, args=(limit,), fetch_response=False)

    def rcon_get_ackslimit(self):
        response = self.send_rcon_command(RCON_ACKSLIMIT)[0]
        return parse_server_var(response)

    def rcon_set_ackslimit(self, limit):
        return self.send_rcon_command(RCON_ACKSLIMIT, args=(limit,), fetch_response=False)

    def rcon_get_messageholelimit(self):
        response = self.send_rcon_command(RCON_MESSAGEHOLELIMIT)[0]
        return parse_server_var(response)

    def rcon_set_messageholelimit(self, limit):
        return self.send_rcon_command(RCON_MESSAGEHOLELIMIT, args=(limit,), fetch_response=False)

    def rcon_get_playertimeout(self):
        response = self.send_rcon_command(RCON_PLAYERTIMEOUT)[0]
        return parse_server_var(response)

    def rcon_set_playertimeout(self, limit):
        return self.send_rcon_command(RCON_PLAYERTIMEOUT, args=(limit,), fetch_response=False)

    def rcon_get_language(self):
        response = self.send_rcon_command(RCON_LANGUAGE)[0]
        return parse_server_var(response)

    def rcon_set_language(self, limit):
        return self.send_rcon_command(RCON_LANGUAGE, args=(limit,), fetch_response=False)
