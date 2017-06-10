from __future__ import unicode_literals, absolute_import
from unittest.case import TestCase

from samp_client import utils


class UtilsTestCase(TestCase):
    def test_encode(self):
        expected = chr(127) + chr(0) + chr(0) + chr(1)
        self.assertEqual(expected, utils.encode_bytes(127, 0, 0, 1))

    def test_decode_int_1(self):
        self.assertEqual(0, utils.decode_int(chr(0)))
        self.assertEqual(16, utils.decode_int(chr(16)))
        self.assertEqual(200, utils.decode_int(chr(200)))


    def test_decode_int_4(self):
        self.assertEqual(7989, utils.decode_int('5\x1f\x00\x00'))

    def test_decode_string(self):
        input = '\x04Test+++'
        expected = 'Test'
        result = utils.decode_string(input, 0, 1)
        self.assertEqual(expected, result)

    def test_decode_string_2(self):
        input = '\x04\x00Test-----'
        expected = 'Test'
        result = utils.decode_string(input, 0, 2)
        self.assertEqual(expected, result)

    def test_decode_string_4(self):
        input = '\x0f\x00\x00\x00Convoy Trucking===='
        expected = 'Convoy Trucking'
        result = utils.decode_string(input, 0, 4)
        self.assertEqual(expected, result)

    def test_decode_string_4_offset_4(self):
        input = '    \x0f\x00\x00\x00Convoy Trucking\x00\x00'
        expected = 'Convoy Trucking'
        result = utils.decode_string(input, 4, 4)
        self.assertEqual(expected, result)