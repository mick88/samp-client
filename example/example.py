from __future__ import unicode_literals, absolute_import, print_function

import sys

from samp_client import constants
from samp_client.client import SampClient


def info(client):
    print("""Server Info:
Password: {info.password}
Players: {info.players}/{info.max_players}
Hostname: {info.hostname}
Gamemode: {info.gamemode}
Language: {info.language}
    """.format(
        info=client.get_server_info(),
    ))


def rules(client):
    print("Server Rules:")
    for rule in client.get_server_rules():
        print("{rule.name}: {rule.value}".format(
            rule=rule,
        ))


def clients(client):
    print("Connected Clients")
    print("Name                       | Score".format(client=client))
    print("==================================")
    for client in client.get_server_clients():
        print("{client.name:26} | {client.score}".format(client=client))


def details(client):
    print("Detailed Clients")
    print(" ID |Name                        | Score | Ping".format(client=client))
    print("===============================================")
    for client in client.get_server_clients_detailed():
        print("{client.id:3} | {client.name:26} | {client.score:5} | {client.ping:4}".format(client=client))


def main(args):
    with SampClient(*args) as client:
        server_info = client.get_server_info()
        print("""Connected to {info.hostname}. 
Currently {info.players}/{info.max_players} players online.

Select one of the options:

i. Server Info
r. Server Rules
c. Connected clients
d. Detailed clients
""".format(
            info=server_info,
        ))

        option = raw_input('Select option: ')
        if option == constants.OPCODE_INFO:
            info(client)
        elif option == constants.OPCODE_RULES:
            rules(client)
        elif option == constants.OPCODE_CLIENTS:
            clients(client)
        elif option == constants.OPCODE_CLIENTS_DETAILED:
            details(client)
        else:
            print('Unknown option, bye!')

main(sys.argv[1:])
