# coding=utf-8
from unittest.case import TestCase
from samp_client import utils
from samp_client.constants import ENCODING


class UtilsTestCase(TestCase):
    def test_encode(self):
        expected = bytes(chr(127) + chr(0) + chr(0) + chr(1), ENCODING)
        self.assertEqual(expected, utils.encode_bytes(127, 0, 0, 1))

    def test_decode_int_1(self):
        self.assertEqual(0, utils.decode_int(chr(0)))
        self.assertEqual(16, utils.decode_int(chr(16)))
        self.assertEqual(200, utils.decode_int(chr(200)))

    def test_decode_int_4(self):
        self.assertEqual(7989, utils.decode_int(b'5\x1f\x00\x00'))

    def test_decode_string(self):
        input = b'\x04Test+++'
        expected = 'Test'
        result = utils.decode_string(input, 0, 1)
        self.assertEqual(expected, result)

    def test_decode_string__unicode(self):
        input = b'\x00\xa2\x00,\x01%\x00\x00\x00- Excellent Dreams Role Play\x99 | VOICE'
        expected = u'- Excellent Dreams Role Play™ | VOICE'

        result = utils.decode_string(input, 0, 9)
        self.assertEqual(expected, result)

    def test_decode_string_2(self):
        input = b'\x04\x00Test-----'
        expected = 'Test'
        result = utils.decode_string(input, 0, 2)
        self.assertEqual(expected, result)

    def test_decode_string_4(self):
        input = b'\x0f\x00\x00\x00Convoy Trucking===='
        expected = 'Convoy Trucking'
        result = utils.decode_string(input, 0, 4)
        self.assertEqual(expected, result)

    def test_decode_string_4_offset_4(self):
        input = b'    \x0f\x00\x00\x00Convoy Trucking\x00\x00'
        expected = 'Convoy Trucking'
        result = utils.decode_string(input, 4, 4)
        self.assertEqual(expected, result)

    def test_build_rcon_command(self):
        self.assertEqual(b'cmdlist', utils.build_rcon_command('cmdlist'))
        self.assertEqual(b'cmdlist', utils.build_rcon_command('cmdlist', args=[]))
        self.assertEqual(b'cmdlist', utils.build_rcon_command('cmdlist', args=tuple()))

    def test_build_rcon_command_string(self):
        self.assertEqual(b'language Polish', utils.build_rcon_command('language', args='Polish'))
        self.assertEqual(b'language Polish', utils.build_rcon_command('language', args=['Polish']))

    def test_build_rcon_command_int(self):
        self.assertEqual(b'kick 5', utils.build_rcon_command('kick', args=5))
        self.assertEqual(b'kick 5', utils.build_rcon_command('kick', args=[5]))
        self.assertEqual(b'kick 0', utils.build_rcon_command('kick', args=0))
        self.assertEqual(b'kick 0', utils.build_rcon_command('kick', args=[0]))

    def test_build_rcon_command_bool(self):
        self.assertEqual(b'test 1', utils.build_rcon_command('test', args=True))
        self.assertEqual(b'test 0', utils.build_rcon_command('test', args=False))

    def test_build_rcon_command_float(self):
        self.assertEqual(b'gravity 0.008', utils.build_rcon_command('gravity', args=0.008))
        self.assertEqual(b'test 0.008', utils.build_rcon_command('test', args=0.008))

    def test_parse_server_var_int(self):
        var = utils.parse_server_var('ackslimit\t= 3000  (int)')
        self.assertEqual('ackslimit', var.name)
        self.assertEqual(3000, var.value)
        self.assertIsInstance(var.value, int)
        self.assertFalse(var.read_only)

    def test_parse_server_var_bool(self):
        var = utils.parse_server_var('announce\t= 0  (bool)')
        self.assertEqual('announce', var.name)
        self.assertEqual(False, var.value)
        self.assertIsInstance(var.value, bool)
        self.assertFalse(var.read_only)

    def test_parse_server_var_bool_true(self):
        var = utils.parse_server_var('announce\t= 1  (bool)')
        self.assertEqual('announce', var.name)
        self.assertEqual(True, var.value)
        self.assertIsInstance(var.value, bool)
        self.assertFalse(var.read_only)

    def test_parse_server_var_string(self):
        var = utils.parse_server_var('gamemode0\t= "convoy"  (string)')
        self.assertEqual('gamemode0', var.name)
        self.assertEqual('convoy', var.value)
        self.assertIsInstance(var.value, str)
        self.assertFalse(var.read_only)

    def test_parse_server_var_float(self):
        var = utils.parse_server_var('stream_distance	= 300.000000  (float)')
        self.assertEqual('stream_distance', var.name)
        self.assertEqual(300.000000, var.value)
        self.assertIsInstance(var.value, float)
        self.assertFalse(var.read_only)

    def test_parse_server_var_readonly(self):
        var = utils.parse_server_var('filterscripts\t= "WeatherStreamer"  (string) (read-only)')
        self.assertTrue(var.read_only)
        self.assertEqual('filterscripts', var.name)
        self.assertEqual('WeatherStreamer', var.value)
        self.assertIsInstance(var.value, str)

    def test_parse_server_var_ip_readonly(self):
        var = utils.parse_server_var('bind\t\t= "127.0.0.1"  (string) (read-only)')
        self.assertTrue(var.read_only)
        self.assertEqual('bind', var.name)
        self.assertEqual('127.0.0.1', var.value)
        self.assertIsInstance(var.value, str)
