# TV Cleanup

This is a container that has one job, cleanup a TV directory. This works by simply deleting any file over a X days old of show Y. It parses a simple config file formated as X,Y.

```(txt)
X,Y
14,Some Show
```

## Usage

Run this container using docker

```(bash)
docker run -d --name tvcleanup \
    -e PUID=1000
    -e PGID=1000
    -e TZ=Europe/London
    -v /path/to/config:/config \
    -v /path/to/tv_shows:/tv \
    flexibletoast/tvcleanup:latest
```

Run using docker-compose

```(yaml)
---
version: "3.0"
services:
  tvcleanup:
    image: flexibletoast/tvcleanup
    container_name: tvcleanup
    environment:
      TZ: Europe/London
      PUID: 1000
      PGID: 1000
    volumes:
      - /path/to/config:/config
      - /path/to/tv_shows:/tv
```

## Parameters

| **Parameter**       | **Function**                |
| ------------------- | --------------------------- |
| -e TZ=Europe/London | Specify a timezone to use   |
| -e PUID=1000        | Specify a user ID           |
| -e PGID=1000        | Specify a group ID          |
| -v /config          | tvclean.conf is stored here |
| -v /tv              | Location of TV library      |
