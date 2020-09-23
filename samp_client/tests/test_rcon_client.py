from unittest import TestCase

from samp_client.models import ServerVar, RConPlayer

from samp_client.client import SampClient
from samp_client.exceptions import InvalidRconPassword, RconError, SampError
from samp_client.tests.mock import MockSocket


class RconClientTestCase(TestCase):
    VAR_LIST = [
        ServerVar(name='ackslimit', value=3000, read_only=False),
        ServerVar(name='announce', value=False, read_only=False), ServerVar(name='bind', value='', read_only=True),
        ServerVar(name='chatlogging', value=1, read_only=False),
        ServerVar(name='conncookies', value=1, read_only=False),
        ServerVar(name='connseedtime', value=300000, read_only=False),
        ServerVar(name='cookielogging', value=0, read_only=False),
        ServerVar(name='db_log_queries', value=0, read_only=False),
        ServerVar(name='db_logging', value=0, read_only=False),
        ServerVar(name='filterscripts', value='WeatherStreamer', read_only=True),
        ServerVar(name='gamemode0', value='convoy', read_only=False),
        ServerVar(name='gamemode1', value='', read_only=False),
        ServerVar(name='gamemode10', value='', read_only=False),
        ServerVar(name='gamemode11', value='', read_only=False),
        ServerVar(name='gamemode12', value='', read_only=False),
        ServerVar(name='gamemode13', value='', read_only=False),
        ServerVar(name='gamemode14', value='', read_only=False),
        ServerVar(name='gamemode15', value='', read_only=False),
        ServerVar(name='gamemode2', value='', read_only=False),
        ServerVar(name='gamemode3', value='', read_only=False),
        ServerVar(name='gamemode4', value='', read_only=False),
        ServerVar(name='gamemode5', value='', read_only=False),
        ServerVar(name='gamemode6', value='', read_only=False),
        ServerVar(name='gamemode7', value='', read_only=False),
        ServerVar(name='gamemode8', value='', read_only=False),
        ServerVar(name='gamemode9', value='', read_only=False),
        ServerVar(name='gamemodetext', value='Convoy Trucking DEV', read_only=False),
        ServerVar(name='gravity', value='0.008', read_only=False),
        ServerVar(name='hostname', value='Convoy Trucking', read_only=False),
        ServerVar(name='incar_rate', value=40, read_only=True),
        ServerVar(name='lagcomp', value='On', read_only=True),
        ServerVar(name='lagcompmode', value=1, read_only=True),
        ServerVar(name='language', value='English', read_only=False),
        ServerVar(name='lanmode', value=False, read_only=False),
        ServerVar(name='logqueries', value=False, read_only=False),
        ServerVar(name='logtimeformat', value='[%d %b %H:%M:%S]', read_only=True),
        ServerVar(name='mapname', value='San Andreas', read_only=False),
        ServerVar(name='maxnpc', value=0, read_only=False), ServerVar(name='maxplayers', value=10, read_only=True),
        ServerVar(name='messageholelimit', value=3000, read_only=False),
        ServerVar(name='messageslimit', value=500, read_only=False),
        ServerVar(name='minconnectiontime', value=0, read_only=False),
        ServerVar(name='myriad', value=False, read_only=False), ServerVar(name='nosign', value='', read_only=True),
        ServerVar(name='onfoot_rate', value=40, read_only=True),
        ServerVar(name='output', value=False, read_only=False),
        ServerVar(name='password', value='', read_only=False),
        ServerVar(name='playertimeout', value=10000, read_only=False),
        ServerVar(name='plugins', value='CVector.so', read_only=True),
        ServerVar(name='port', value=7777, read_only=True), ServerVar(name='query', value=True, read_only=False),
        ServerVar(name='rcon', value=True, read_only=False),
        ServerVar(name='rcon_password', value='password', read_only=False),
        ServerVar(name='sleep', value=5, read_only=False),
        ServerVar(name='stream_distance', value=300.0, read_only=False),
        ServerVar(name='stream_rate', value=1000, read_only=False),
        ServerVar(name='timestamp', value=True, read_only=False),
        ServerVar(name='version', value='0.3.7-R2', read_only=True),
        ServerVar(name='weapon_rate', value=40, read_only=True),
        ServerVar(name='weather', value='10', read_only=False),
        ServerVar(name='weburl', value='localhost:8000', read_only=False),
        ServerVar(name='worldtime', value='10:00', read_only=False),
    ]

    def setUp(self):
        super(RconClientTestCase, self).setUp()
        self.client = SampClient(address='localhost', rcon_password='password')
        self.client.socket_cls = MockSocket
        self.client.connect()

    def tearDown(self):
        super(RconClientTestCase, self).tearDown()
        self.client.disconnect()

    def test_no_password(self):
        self.client.rcon_password = None
        self.assertRaises(RconError, self.client.rcon_players)

    def test_incorrect_password(self):
        self.client.rcon_password = 'invalidpassword'
        self.assertRaises(InvalidRconPassword, self.client.rcon_players)

    def test_rcon_password_bytes(self):
        self.client.rcon_password = 'password'
        self.assertEqual(self.client.rcon_password_bytes, b'\x08\x00password', )

    def test_rcon_cmdlist(self):
        response = self.client.rcon_cmdlist()
        self.assertEqual(response, [
            'echo', 'exec', 'cmdlist', 'varlist', 'exit', 'kick', 'ban', 'gmx', 'changemode', 'say',
            'reloadbans', 'reloadlog', 'players', 'banip', 'unbanip', 'gravity', 'weather', 'loadfs',
            'unloadfs', 'reloadfs',
        ])

    def test_rcon_varlist(self):
        varlist = self.client.rcon_varlist()
        self.assertEqual(varlist, self.VAR_LIST)

    def test_rcon_varlist_dict(self):
        vardict = self.client.rcon_varlist_dict()
        expected_dict = {var.name: var.value for var in self.VAR_LIST}
        self.assertEqual(vardict, expected_dict)

    def test_rcon_exit(self):
        response = self.client.rcon_exit()
        self.assertIsNone(response)

    def test_rcon_echo(self):
        response = self.client.rcon_echo('Hello')
        self.assertEqual(response, 'Hello')

    def test_rcon_set_hostname(self):
        response = self.client.rcon_set_hostname('test hostname')
        self.assertIsNone(response)
        self.client.rcon_set_hostname('Convoy Trucking')

    def test_rcon_get_hostname(self):
        hostname = self.client.rcon_get_hostname()
        self.assertEqual(hostname, ServerVar('hostname', 'Convoy Trucking', False))

    def test_rcon_set_gamemodetext(self):
        response = self.client.rcon_set_gamemodetext('New Gamemode')
        self.assertIsNone(response)
        response = self.client.rcon_set_gamemodetext('Convoy Trucking DEV')

    def test_rcon_get_gamemodetext(self):
        var = self.client.rcon_get_gamemodetext()
        self.assertEqual(var, ServerVar('gamemodetext', 'Convoy Trucking DEV', False))

    def test_rcon_set_mapname(self):
        response = self.client.rcon_set_mapname('Convoy map')
        self.assertIsNone(response)
        self.client.rcon_set_mapname('San Andreas')

    def test_rcon_get_mapname(self):
        response = self.client.rcon_get_mapname()
        self.assertEqual(response, ServerVar(name='mapname', value='San Andreas', read_only=False))

    def test_rcon_exec(self):
        response = self.client.rcon_exec('server')
        self.assertEqual(response, ['bind = ""  (string, read-only)', 'password = ""  (string)',
                                    'maxplayers = 10  (int, read-only)', 'port = 7777  (int, read-only)',
                                    'filterscripts = "WeatherStreamer"  (string, read-only)',
                                    'plugins = "CVector.so"  (string, read-only)', 'onfoot_rate = 40  (int, read-only)',
                                    'incar_rate = 40  (int, read-only)', 'weapon_rate = 40  (int, read-only)',
                                    'logtimeformat = "[%d %b %H:%M:%S]"  (string, read-only)'])

    def test_rcon_exec__invalid(self):
        with self.assertRaises(SampError):
            self.client.rcon_exec('invalid')

    def test_rcon_kick(self):
        response = self.client.rcon_kick(0)
        self.assertEqual(response, [
            'mick88 <#0 - 172.19.0.1> has been kicked.',
            'Logged time spent online for mick88: 0 min',
            'mick88 left the server (Kicked)',
            'wanted level set to 0',
            '[part] mick88 has left the server (0:2)',
        ])

    def test_rcon_kick__invalidid(self):
        response = self.client.rcon_kick(999)
        self.assertEqual(response, [])

    def test_rcon_ban(self):
        response = self.client.rcon_ban(0)
        self.assertEqual(response, [
            'mick88 <#0 - 172.19.0.1> has been banned.',
            'Logged time spent online for mick88: 0 min',
            'mick88 left the server (Kicked)',
            'wanted level set to 0',
            '[part] mick88 has left the server (0:2)',
        ])

    def test_rcon_ban__invalid(self):
        response = self.client.rcon_ban(999)
        self.assertEqual(response, [])

    def test_rcon_banip(self):
        response = self.client.rcon_banip('192.168.1.1')
        self.assertEqual(response, ['IP 192.168.1.1 has been banned.'])

    def test_rcon_unbanip(self):
        response = self.client.rcon_unbanip('192.168.1.1')
        self.assertEqual(response, [])

    def test_rcon_changemode(self):
        response = self.client.rcon_changemode('convoy')
        self.assertEqual(response, [])

    def test_rcon_changemode__invalid(self):
        response = self.client.rcon_changemode('invalid')
        self.assertEqual(response, [])

    def test_rcon_gmx(self):
        response = self.client.rcon_gmx()
        self.assertEqual(response, [])

    def test_rcon_reloadbans(self):
        response = self.client.rcon_reloadbans()
        self.assertEqual(response, [])

    def test_rcon_reloadlog(self):
        response = self.client.rcon_reloadlog()
        self.assertEqual(response, [])

    def test_rcon_say(self):
        response = self.client.rcon_say('Hello')
        self.assertEqual(response, [])

    def test_rcon_players(self):
        response = self.client.rcon_players()
        self.assertEqual(response, [RConPlayer(id=0, name='mick88', ping=15, ip='172.18.0.1')])

    def test_rcon_gravity(self):
        response = self.client.rcon_gravity(0.008)
        self.assertEqual(response, [])

    def test_rcon_weather(self):
        response = self.client.rcon_weather(1)
        self.assertEqual(response, [])

    def test_rcon_loadfs(self):
        response = self.client.rcon_loadfs('WeatherStreamer')
        self.assertEqual(response, "Filterscript 'WeatherStreamer.amx' loaded.")

    def test_rcon_loadfs__invalid(self):
        with self.assertRaises(SampError):
            self.client.rcon_loadfs('invalid')

    def test_rcon_unloadfs(self):
        response = self.client.rcon_unloadfs('WeatherStreamer')
        self.assertEqual(response, "Filterscript 'WeatherStreamer.amx' unloaded.")

    def test_rcon_reloadfs(self):
        response = self.client.rcon_reloadfs('WeatherStreamer')
        self.assertEqual(response, [
            "Filterscript 'WeatherStreamer.amx' unloaded.",
            "Filterscript 'WeatherStreamer.amx' loaded.",
        ])

    def test_rcon_get_weburl(self):
        response = self.client.rcon_get_weburl()
        self.assertEqual(response, ServerVar(name='weburl', value='localhost:8000', read_only=False))

    def test_rcon_set_weburl(self):
        response = self.client.rcon_set_weburl('convoytrucking.net')
        self.assertEqual(response, [])

    def test_rcon_set_rcon_password(self):
        response = self.client.rcon_set_rcon_password('newpass')
        self.assertIsNone(response)
        self.assertEqual(self.client.rcon_password, 'newpass')

    def test_rcon_get_rcon_password(self):
        response = self.client.rcon_get_rcon_password()
        self.assertEqual(response, ServerVar(name='rcon_password', value='password', read_only=False))

    def test_rcon_get_password(self):
        response = self.client.rcon_get_password()
        # Server has no password
        self.assertEqual(response, ServerVar(name='password', value='', read_only=False))

    def test_rcon_set_password(self):
        response = self.client.rcon_set_password('pass')
        self.assertEqual(response, 'Setting server password to: "pass"')

    def test_rcon_get_messageslimit(self):
        response = self.client.rcon_get_messageslimit()
        self.assertEqual(response, ServerVar(name='messageslimit', value=500, read_only=False))

    def test_rcon_set_messageslimit(self):
        response = self.client.rcon_set_messageslimit(200)
        self.assertIsNone(response)

    def test_rcon_get_ackslimit(self):
        response = self.client.rcon_get_ackslimit()
        self.assertEqual(response, ServerVar(name='ackslimit', value=3000, read_only=False))

    def test_rcon_set_ackslimit(self):
        response = self.client.rcon_set_ackslimit(1000)
        self.assertIsNone(response)

    def test_rcon_get_messageholelimit(self):
        response = self.client.rcon_get_messageholelimit()
        self.assertEqual(response, ServerVar(name='messageholelimit', value=3000, read_only=False))

    def test_rcon_set_messageholelimit(self):
        response = self.client.rcon_set_messageholelimit(1000)
        self.assertIsNone(response)

    def test_rcon_get_playertimeout(self):
        response = self.client.rcon_get_playertimeout()
        self.assertEqual(response, ServerVar(name='playertimeout', value=10000, read_only=False))

    def test_rcon_set_playertimeout(self):
        response = self.client.rcon_set_playertimeout(1000)
        self.assertIsNone(response)

    def test_rcon_get_language(self):
        response = self.client.rcon_get_language()
        self.assertEqual(response, ServerVar(name='language', value='English', read_only=False))

    def test_rcon_set_language(self):
        response = self.client.rcon_set_language('Polish')
        self.assertIsNone(response)
