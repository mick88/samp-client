from __future__ import unicode_literals, absolute_import
from samp_client.client import SampClient

with SampClient(address='server.convoytrucking.net') as client:
    server_info = client.get_server_info()
    print repr(server_info)