# pingtop
tiny top like program that visualises the ping to a host

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

## DOCKER BUILD & RUN

cd into the cloned repository dir
```bash
docker build -t pingtop ./
```

run
```bash
docker run -it -e HOST='twitch.tv' pingtop
```

