# GTA SA-MP client 

## RCON and query client library for  Python

A modern Python library for querying and managing SA-MP servers.
 
Supported Python version 3.6 or newer. 
If you require support for Python 2.7, install 2.1 version of the package.

### Installation
```bash
pip install samp-client
```

### Usage
The library can be easily interfaced using a single `SampClient` class:

```python
from samp_client.client import SampClient

with SampClient(address='localhost', port=7777) as client:
    print(client.get_server_info())
```

The library also allows you to run RCON commands as well as queries:
```python
from samp_client.client import SampClient

with SampClient(address='localhost', port=7777, rcon_password='password') as client:
    client.rcon_cmdlist()
```

Query and RCON responses are parsed into native Python structures:
```python
from samp_client.client import SampClient

with SampClient(address='localhost', port=7777, rcon_password='password') as client:
    info = client.get_server_info()
    print(info)
    # ServerInfo(password=True, players=9, max_players=100, hostname='Convoy Trucking', gamemode='Convoy Trucking 3.1.1', language='English')
    print(info.gamemode)
    # 'Convoy Trucking 3.1.1'
    print(client.rcon_get_hostname())
    # ServerVar(name='hostname', value='Convoy Trucking', read_only=False)
    print(client.rcon_players()[0].ping)
    # 26
```


### Examples
Folder `example/` contains usage example of the library

### Running tests
To run tests:
```bash
python -m unittest discover -v
```
