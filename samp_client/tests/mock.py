class MockSocket(object):
    responses = {
        b'SAMP3\xfe\x82\x0ea\x1eptest': b'test',
        b'SAMP3\xfe\x82\x0ea\x1ec': b"\x0c\x00\x0bpedr$$Nn157_G\x00\x00\x04SuBa\x9c\x03\x00\x00\tChocolateW\x1e\x00\x00\x0cbiieL$iNn157YG\x00\x00\x0bMartin80nik\xd0'\x00\x00\x0cNadoVGs(AFK)*\x14\x00\x00\x04Ottof\x00\x00\x00\x0bKristo_Rand\x01\x00\x00\x00\x07abeceda\x02\x00\x00\x00\x08katerina\x00\x00\x00\x00\x11Jonas_Nicholls_II5l\x00\x00\nMurs_Beten\x81\x02\x00\x00",
        b'SAMP3\xfe\x82\x0ea\x1ed': b"\x0c\x00\x00\x0bpedr$$Nn157_G\x00\x00\xfc\x00\x00\x00\x01\x04SuBa\x9c\x03\x00\x008\x00\x00\x00\x02\tChocolateW\x1e\x00\x00\x18\x00\x00\x00\x03\x0cbiieL$iNn157YG\x00\x00\xe4\x00\x00\x00\x04\x0bMartin80nik\xd0'\x00\x00H\x00\x00\x00\x05\x0cNadoVGs(AFK)*\x14\x00\x00\xd4\x00\x00\x00\x08\x04Ottof\x00\x00\x00j\x00\x00\x00\t\x0bKristo_Rand\x01\x00\x00\x00P\x00\x00\x00\n\x07abeceda\x02\x00\x00\x00:\x00\x00\x00\x0b\x08katerina\x00\x00\x00\x00F\x00\x00\x00\x0c\x11Jonas_Nicholls_II5l\x00\x00B\x00\x00\x00\x0e\nMurs_Beten\x81\x02\x00\x007\x00\x00\x00",
        b'SAMP3\xfe\x82\x0ea\x1ei': b'\x00\x0c\x00d\x00\x0f\x00\x00\x00Convoy Trucking\x15\x00\x00\x00Convoy Trucking 3.4.4\x07\x00\x00\x00English',
        b'SAMP3\xfe\x82\x0ea\x1er': b'\x06\x00\x07lagcomp\x02On\x07mapname\x0bSan Andreas\x07version\x080.3.7-R2\x07weather\x0210\x06weburl\x16www.convoytrucking.net\tworldtime\x0518:00',
        # RCON
        b'SAMP3\xfe\x82\x0ea\x1ex\x0f\x00invalidpassword\x07\x00players': b'\x16\x00Invalid RCON password.',
        b'SAMP\x7f\x00\x00\x01a\x1ex\x0f\x00invalidpassword\x07\x00players': [b'\x16\x00Invalid RCON password.', None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x05\x00ban 0': [b')\x00mick88 <#0 - 172.19.0.1> has been banned.', b'*\x00Logged time spent online for mick88: 0 min', b'\x1f\x00mick88 left the server (Kicked)', b'\x16\x00 wanted level set to 0', b"'\x00[part] mick88 has left the server (0:2)", None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x07\x00ban 999': [None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x11\x00banip 192.168.1.1': [
            b'\x1f\x00IP 192.168.1.1 has been banned.', None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x11\x00changemode convoy': [None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x12\x00changemode invalid': [None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x07\x00cmdlist': [b'\x11\x00Console Commands:', b'\x06\x00  echo', b'\x06\x00  exec', b'\t\x00  cmdlist', b'\t\x00  varlist', b'\x06\x00  exit', b'\x06\x00  kick', b'\x05\x00  ban', b'\x05\x00  gmx', b'\x0c\x00  changemode', b'\x05\x00  say', b'\x0c\x00  reloadbans', b'\x0b\x00  reloadlog', b'\t\x00  players', b'\x07\x00  banip', b'\t\x00  unbanip', b'\t\x00  gravity', b'\t\x00  weather', b'\x08\x00  loadfs', b'\n\x00  unloadfs', b'\n\x00  reloadfs', b'\x00\x00'],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\n\x00echo Hello': [b'\x05\x00Hello', None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x0b\x00exec server': [b'\x1e\x00bind = ""  (string, read-only)', b'\x17\x00password = ""  (string)', b'!\x00maxplayers = 10  (int, read-only)', b'\x1d\x00port = 7777  (int, read-only)', b'6\x00filterscripts = "WeatherStreamer"  (string, read-only)', b'+\x00plugins = "CVector.so"  (string, read-only)', b'"\x00onfoot_rate = 40  (int, read-only)', b'!\x00incar_rate = 40  (int, read-only)', b'"\x00weapon_rate = 40  (int, read-only)', b'7\x00logtimeformat = "[%d %b %H:%M:%S]"  (string, read-only)', None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x0c\x00exec invalid': [b'"\x00Unable to exec file \'invalid.cfg\'.', None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\t\x00ackslimit': [b'\x17\x00ackslimit = 3000  (int)', None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x0c\x00gamemodetext': [b'.\x00gamemodetext = "Convoy Trucking DEV"  (string)', None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x08\x00hostname': [b'&\x00hostname = "Convoy Trucking"  (string)', None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x08\x00language': [b'\x1e\x00language = "English"  (string)', None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x07\x00mapname': [b'!\x00mapname = "San Andreas"  (string)', None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x10\x00messageholelimit': [b'\x1e\x00messageholelimit = 3000  (int)', None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\r\x00messageslimit': [b'\x1a\x00messageslimit = 500  (int)', None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x08\x00password': [b'\x17\x00password = ""  (string)', None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\r\x00playertimeout': [b'\x1c\x00playertimeout = 10000  (int)',
                                                                           None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\r\x00rcon_password': [
            b'$\x00rcon_password = "password"  (string)', None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x06\x00weburl': [b'#\x00weburl = "localhost:8000"  (string)',
                                                                      None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x03\x00gmx': [None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\r\x00gravity 0.008': [None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x06\x00kick 0': [b')\x00mick88 <#0 - 172.19.0.1> has been kicked.', b'*\x00Logged time spent online for mick88: 0 min', b'\x1f\x00mick88 left the server (Kicked)', b'\x16\x00 wanted level set to 0', b"'\x00[part] mick88 has left the server (0:2)", None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x08\x00kick 999': [None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x16\x00loadfs WeatherStreamer': [b",\x00  Filterscript 'WeatherStreamer.amx' loaded.", None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x0e\x00loadfs invalid': [b")\x00  Filterscript 'invalid.amx' load failed.", None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x07\x00players': [b'\x0f\x00ID\tName\tPing\tIP', b'\x16\x000\tmick88\t15\t172.19.0.1', None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\n\x00reloadbans': [None, None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x18\x00reloadfs WeatherStreamer': [b".\x00  Filterscript 'WeatherStreamer.amx' unloaded.", b",\x00  Filterscript 'WeatherStreamer.amx' loaded.", None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\t\x00say Hello': [None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\r\x00password pass': [b'"\x00Setting server password to: "pass"', None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x15\x00rcon_password newpass': [None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x19\x00weburl convoytrucking.net': [None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x13\x00unbanip 192.168.1.1': [None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x18\x00unloadfs WeatherStreamer': [
            b".\x00  Filterscript 'WeatherStreamer.amx' unloaded.", None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\t\x00weather 1': [None],
        b'SAMP\x7f\x00\x00\x01a\x1ex\x08\x00password\x07\x00varlist': [b'\x12\x00Console Variables:', b'\x19\x00  ackslimit\t= 3000  (int)', b'\x16\x00  announce\t= 0  (bool)', b'"\x00  bind\t\t= ""  (string) (read-only)', b'\x18\x00  chatlogging\t= 1  (int)', b'\x18\x00  conncookies\t= 1  (int)', b'\x1e\x00  connseedtime\t= 300000  (int)', b'\x1a\x00  cookielogging\t= 0  (int)', b'\x1b\x00  db_log_queries\t= 0  (int)', b'\x17\x00  db_logging\t= 0  (int)', b'9\x00  filterscripts\t= "WeatherStreamer"  (string) (read-only)', b' \x00  gamemode0\t= "convoy"  (string)', b'\x1a\x00  gamemode1\t= ""  (string)', b'\x1b\x00  gamemode10\t= ""  (string)', b'\x1b\x00  gamemode11\t= ""  (string)', b'\x1b\x00  gamemode12\t= ""  (string)', b'\x1b\x00  gamemode13\t= ""  (string)', b'\x1b\x00  gamemode14\t= ""  (string)', b'\x1b\x00  gamemode15\t= ""  (string)', b'\x1a\x00  gamemode2\t= ""  (string)', b'\x1a\x00  gamemode3\t= ""  (string)', b'\x1a\x00  gamemode4\t= ""  (string)', b'\x1a\x00  gamemode5\t= ""  (string)', b'\x1a\x00  gamemode6\t= ""  (string)', b'\x1a\x00  gamemode7\t= ""  (string)', b'\x1a\x00  gamemode8\t= ""  (string)', b'\x1a\x00  gamemode9\t= ""  (string)', b'0\x00  gamemodetext\t= "Convoy Trucking DEV"  (string)', b'\x1d\x00  gravity\t= "0.008"  (string)', b'(\x00  hostname\t= "Convoy Trucking"  (string)', b'$\x00  incar_rate\t= 40  (int) (read-only)', b'-\x00  lagcomp\t= "On"  (string) (read-only) (rule)', b'$\x00  lagcompmode\t= 1  (int) (read-only)', b' \x00  language\t= "English"  (string)', b'\x15\x00  lanmode\t= 0  (bool)', b'\x18\x00  logqueries\t= 0  (bool)', b':\x00  logtimeformat\t= "[%d %b %H:%M:%S]"  (string) (read-only)', b'*\x00  mapname\t= "San Andreas"  (string) (rule)', b'\x13\x00  maxnpc\t= 0  (int)', b'$\x00  maxplayers\t= 10  (int) (read-only)', b' \x00  messageholelimit\t= 3000  (int)', b'\x1c\x00  messageslimit\t= 500  (int)', b'\x1e\x00  minconnectiontime\t= 0  (int)', b'\x14\x00  myriad\t= 0  (bool)', b'#\x00  nosign\t= ""  (string) (read-only)', b'%\x00  onfoot_rate\t= 40  (int) (read-only)', b'\x14\x00  output\t= 0  (bool)', b'\x19\x00  password\t= ""  (string)', b'\x1e\x00  playertimeout\t= 10000  (int)', b'.\x00  plugins\t= "CVector.so"  (string) (read-only)', b'!\x00  port\t\t= 7777  (int) (read-only)', b'\x14\x00  query\t\t= 1  (bool)', b'\x13\x00  rcon\t\t= 1  (bool)', b'&\x00  rcon_password\t= "password"  (string)', b'\x13\x00  sleep\t\t= 5  (int)', b"'\x00  stream_distance\t= 300.000000  (float)", b'\x1b\x00  stream_rate\t= 1000  (int)', b'\x17\x00  timestamp\t= 1  (bool)', b'3\x00  version\t= "0.3.7-R2"  (string) (read-only) (rule)', b'%\x00  weapon_rate\t= 40  (int) (read-only)', b'!\x00  weather\t= "10"  (string) (rule)', b',\x00  weburl\t= "localhost:8000"  (string) (rule)', b'&\x00  worldtime\t= "12:00"  (string) (rule)', b'\x00\x00'],
    }
    response_prefix = b'SAMP3\xfe\x82\x0ea\x1ex'

    def __init__(self, *args, **kwargs):
        self.connected = True

    def settimeout(self, value):
        pass

    def close(self):
        self.connected = False
        self.request = False

    def sendto(self, data, *args, **kwargs):
        assert self.connected
        self.request = data

    def recv(self, bufsize):
        assert self.connected
        try:
            response = self.response_prefix
            if self.request:
                value = self.responses[self.request]
                if isinstance(value, list):
                    try:
                        value = value.pop(0) or b''
                    except IndexError:
                        value = b''
                response += value
            return response
        except KeyError:
            raise ConnectionError(10054, 'Connection error')
