from __future__ import unicode_literals, absolute_import


class SampError(Exception):
    pass


class RconError(SampError):
    pass


class InvalidRconPassword(RconError):
    pass