# Bad-Word Filtering in MiniNet

This implementation is designed for filtering offensive language in HTTP responses using MiniNet. It's a practical solution for maintaining decorum in network communications.

## Key Commands
- **Initiate MiniNet Topology**: `sudo python3 topo.py`
- **Accessing Terminals in MiniNet**:
  - `xterm h1` for host terminal
  - `xterm r` for router
  - `xterm server1` for server
- **Client-Side Script**: `python3 client-http.py`
  - `--long`: Requests large HTTP responses.
  - `--mark_time`: Logs time elapsed during requests.
  - `--verbose`: Suppresses request outputs when not used.
  - `--number_of_requests n`: Repeats the requests 'n' times.
  - `--plot`: Displays graphs of request times and their moving averages.
- **Server-Side Script**: `python3 server-http.py`
- **Router Script with Bad-Word Filtering**: `python3 router.py --filter_badwords`
- **Router Script without Filtering**: `python3 router.py`

## Pre-Run Setup
- **Installation of Dependencies**: Ensure to use `sudo` for all `pip3` installations, as MiniNet requires superuser privileges.
  - Install `scapy` via `pip3` (sudo mode).
  - Install `mininet` using `apt`.
  - Install `matplotlib` using `sudo` (sudo mode).

## Sample Content

### HTML File on Server
```
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>Hello from Server 1</h1>
    <p>This is a test page served from server1. fuck you, you fuck, you fucking cunt</p>
</body>
</html>
```

### HTML File as Received by Client
```
<!DOCTYPE html>
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>Hello from Server 1</h1>
    <p>This is a test page served from server1. **** you, you ****, you ****ing ****</p>
</body>
</html>
```


