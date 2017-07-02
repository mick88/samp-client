from __future__ import unicode_literals, absolute_import

from unittest import TestCase
from future.builtins import str

from samp_client.client import SampClient
from samp_client.models import ServerInfo, Rule, Client, ClientDetail


class ClientTestCase(TestCase):
    def setUp(self):
        super(ClientTestCase, self).setUp()
        self.client = SampClient(address='server.convoytrucking.net')
        self.client.connect()

    def tearDown(self):
        super(ClientTestCase, self).tearDown()
        self.client.disconnect()

    def test_server_ip(self):
        # Server address should be changed to ip address
        self.assertNotEqual('server.convoytrucking.net', self.client.address)
        self.assertEqual('51.254.130.14', self.client.address)

    def test_server_info(self):
        info = self.client.get_server_info()
        self.assertIsNotNone(info)
        self.assertIsInstance(info, ServerInfo)
        self.assertIsInstance(info.password, bool)
        self.assertIsInstance(info.players, int)
        self.assertIsInstance(info.max_players, int)
        self.assertIsInstance(info.hostname, str)
        self.assertIsInstance(info.gamemode, str)
        self.assertIsInstance(info.language, str)

        self.assertTrue(info.max_players)
        self.assertTrue(info.hostname)
        self.assertTrue(info.gamemode)
        self.assertTrue(info.language)

    def test_server_rules(self):
        rules = list(self.client.get_server_rules())
        self.assertEqual(6, len(rules))
        self.assertIsNotNone(rules)
        self.assertIsInstance(rules[0], Rule)

    def test_server_rules_dict(self):
        rules = self.client.get_server_rules_dict()
        self.assertIsNotNone(rules)
        self.assertIsInstance(rules, dict)
        self.assertIn('worldtime', rules)
        self.assertIn('mapname', rules)
        self.assertIn('version', rules)
        self.assertIn('weather', rules)

    def test_server_clients(self):
        for client in self.client.get_server_clients():
            self.assertIsInstance(client, Client)
            self.assertIsInstance(client.name, str)
            self.assertIsInstance(client.score, int)
            return # only need to test first yielded client

    def test_server_clients_detailed(self):
        for client in self.client.get_server_clients_detailed():
            self.assertIsInstance(client, ClientDetail)
            self.assertIsInstance(client.name, str)
            self.assertIsInstance(client.score, int)
            self.assertIsInstance(client.ping, int)
            self.assertIsInstance(client.id, int)
            return # only need to test first yielded client
