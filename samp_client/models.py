from __future__ import absolute_import, unicode_literals
from collections import namedtuple

ServerInfo = namedtuple('ServerInfo', ['password', 'players', 'max_players', 'hostname', 'gamemode', 'language'])
Rule = namedtuple('Rule', ['name', 'value'])
Client = namedtuple('Client', ['name', 'score'])
ClientDetail = namedtuple('ClientDetail', ['id', 'name', 'score', 'ping'])
RConPlayer = namedtuple('RConPlayer', ['id', 'name', 'ping', 'ip'])
ServerVar = namedtuple('ServerVar', ['name', 'value', 'read_only'])