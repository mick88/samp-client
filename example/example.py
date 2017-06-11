from __future__ import unicode_literals, absolute_import
from samp_client.client import SampClient

with SampClient(address='localhost', rcon_password='123') as client:
    print client.rcon_get_language()