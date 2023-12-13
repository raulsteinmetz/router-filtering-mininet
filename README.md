# bad-word filtering mininet

this code implements bad word filtering for http responses

important commands:
- sudo python3 topo.py (starts mininet topology)
- iperf -c 8.8.8.8 -c 8888 (check package behaviour on 3 layer)
- xterm h1 for host terminal inside mininet, xterm r for router, xterm server1 for server
- python3 client-http.py on client side (requests for server)
    -- long -> argument that asks for big http responses, if not passed, the requests will be for short messages
    -- mark_time -> marks time relapsed during requests
    -- verbose -> when not called, supresses curl prints
    -- number_of_requests n -> will repeat the requests n times
    -- plot -> plots request times and moving average
- python3 server-http.py on server side (listens and respondes)
- python3 router.py --filter_badwords (router main with activated filter)
- python3 router.py (router main without filter)

if you are going to run it:
- make sure to install all pip3 packages with sudo cause mininet only runs on sudo
- download scapy with pip3 (sudo mode)
- download mininet from apt
- download curl from apt
- download mininet with pip3 (sudo mode)
- download matplotlib with sudo (sudo mode)

