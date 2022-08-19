[TOC]

# FATE EXAMPLE

[FATE](https://github.com/FederatedAI/FATE)

## FATE standalone deploy guide Using docker image

can refer to the [link](https://github.com/FederatedAI/FATE/tree/master/deploy/standalone-deploy)

### Check 8080 port

```bash
lsof -i:8080
```

### Pull mirrors

```bash
export version=1.8.0
docker pull federatedai/standalone_fate:${version}
```

### Execute docker and enter container

```bash
docker run -d --name standalone_fate -p 8080:8080 federatedai/standalone_fate:${version}

# if you want to use jupyter you can add port mapping
# example:
# docker run -d --name standalone_fate -p 8080:8080 -p 8889:8889 federatedai/standalone_fate:${version}
docker exec -it standalone_fate bash

# location of fate is /data/projects/fate

# or you can:
# docker ps -a
# find the name of standalone_fate docker
# docker exec -it name_of_standalone_fate bash
```

### start fate_flow_server

```bash
cd /data/projects/fate/fateflow/bin
sh service.sh status
# if port is not listening
sh service,sh start
```

## Run pipeline example

### using pipeline connect to fate flow service

**bash**:

```bash
pipeline init --ip 127.0.0.1 --port 9380
```