## Create ssh key-less access

```bash
ssh-keygen

ssh-copy-id -i ~/.ssh/id_rsa.pub root@172.168.3.118
```
## Download docker compose
```python
wget https://github.com/docker/compose/releases/download/v2.10.2/docker-compose-linux-x86_64

mv docker-compose-linux-x86_64 /usr/local/bin/docker-compose
```

## Download kubefate and unzip

```bash
wget https://github.com/FederatedAI/KubeFATE/releases/download/v1.8.0-a/kubefate-docker-compose-v1.8.0-a.tar.gz

tar xzvf kubefate-docker-compose-v1.8.0-a.tar.gz
```

## Edit party conf

```bash
cd docker-deploy

vim parties.conf
```
**Parties.conf will be like below [if user is non-root, make sure user has permision to make dir in `/data/projects/fate`]:**

```conf
user=root
dir=/data/projects/fate
party_list=(10000 9999)
party_ip_list=(172.168.3.118 172.168.3.117)
serving_ip_list=(172.168.3.118 172.168.3.117)

enabled_nn=true
```

## Deploy

```bash
sh generate_config.sh

sh docker-deploy.sh all

# or we can deploy the training and serving part seperately
# sh docker_deploy.sh all --training
# sh docker_deploy.sh all --serving
```

## Verify

**in party which party_id=10000**

```bash
docker exec -it confs-10000_client_1 bash
flow test toy --guest-party-id 10000 --host-party-id 9999
```

## Install vim(optional)

**if using proxy, pls unset it when you want to submit fate job **

```bash
apt-get update && apt-get install apt-file -y && apt-file update && apt-get install vim
```

