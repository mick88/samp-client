from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from samp_client.client import SampClient


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
        