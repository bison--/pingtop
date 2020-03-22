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

## DOCKER BUILD & RUN

cd into the cloned repository dir
```bash
docker build -t pingtop ./
```

run
```bash
docker run -it -e HOST='twitch.tv' pingtop
```

## CROSS-LINKS

On dockerhub: https://hub.docker.com/repository/docker/generalbison/pingtop  
On github: https://github.com/bison--/pingtop
