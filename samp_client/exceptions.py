from __future__ import unicode_literals, absolute_import


class SampError(Exception):
    pass


class RconError(SampError):
    pass


class InvalidRconPassword(RconError):
    pass


class ConnectionError(SampError):
    def __init__(self, socket_error):
        self.socket_error = socket_error
        self.err_no, self.message = socket_error.args
        if self.err_no == 10054:
            self.message = 'Server appears to be offline'
        super(ConnectionError, self).__init__(self.message)