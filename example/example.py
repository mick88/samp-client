from __future__ import unicode_literals, absolute_import
from samp_client.client import SampClient

with SampClient(address='server.convoytrucking.net') as client:
    server_info = client.get_server_info()
    print repr(server_info)

    print 'Rules:'
    for rule in client.get_server_rules():
        print '{}={}'.format(
            rule.name,
            rule.value,
        )

    print 'Connected players:'
    for player in client.get_server_clients():
        print '{} ({})'.format(player.name, player.score)


    print 'Connected players (detailed):'
    for player in client.get_server_clients_detailed():
        print repr(player)
