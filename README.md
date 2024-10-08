# pingtop
tiny top like program that visualizes the ping to a host

## RUN

Needs python3 and PING  
cd into the cloned repository dir and run start.py
```bash
./start.py
```

Specify a host to ping with "--host"
```bash
./start.py --host "twitch.tv"
```

```bash
python3 .\start.py --host 'heise.de' --mode 2 --port 80
```

### advanced / help

```
usage: start.py [-h] [--host HOST] [--mode PING_MODE] [--port TCP_PING_PORT]
                [--log SAVE_LOG_PATH]

show a PING graph for a specified host. 8.8.8.8 is default if none is specified.

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           specify the HOST to ping, name or IP
  --mode PING_MODE      what ping method to use, available:
                        1: shell (system ping)
                        2: TCP PING (needs a host with an open port, default: 80)
                        3: python module
  --port TCP_PING_PORT  the port TCP PING should connect
  --log SAVE_LOG_PATH   the full or relative PATH where the log should be written to
                        Examples:
                        --log pingtest.csv
                        --log /var/logs/pingtest.csv
```

## DOCKER 

### RUN

Run the pre-build container directly from dockerhub:
```bash
docker run -it --rm generalbison/pingtop --host twitch.tv --mode 2
```

### BUILD and RUN

cd into the cloned repository dir
```bash
docker build -t pingtop ./
```

run
```bash
docker run -it --rm -e HOST=twitch.tv pingtop
```

```bash
docker run -it --rm pingtop --host twitch.tv
```

## CROSS-LINKS

On dockerhub: https://hub.docker.com/r/generalbison/pingtop
On gitHub: https://github.com/bison--/pingtop

# TODO

## features

* TLS handshake ping
* DNS resolve ping
