# pingtop
tiny top like program that visualises the ping to a host

## BUILD & RUN

cd into the cloned repository dir
```bash
docker build -t pingtop ./
```

run
```bash
docker run -it -e HOST='twitch.tv' pingtop
```

