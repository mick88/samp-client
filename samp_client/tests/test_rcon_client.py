from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from samp_client.client import SampClient
from samp_client.exceptions import SampError, InvalidRconPassword, RconError
from samp_client.models import ServerInfo, Rule, Client, ClientDetail


class RconClientTestCase(TestCase):
    def setUp(self):
        super(RconClientTestCase, self).setUp()
        self.client = SampClient(address='server.convoytrucking.net')
        self.client.connect()

    def tearDown(self):
        super(RconClientTestCase, self).tearDown()
        self.client.disconnect()

    def test_no_password(self):
        self.assertRaises(RconError, self.client.rcon_players)

    def test_incorrect_password(self):
        self.client.rcon_password = 'invalidpassword'
        self.assertRaises(InvalidRconPassword, self.client.rcon_players)
