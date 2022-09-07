# Run example using DSL json conf
## Submit job using exsiting data
### upload data
```bash
# confs-{party-id}-client-1

# in guest
docker exec -it confs-9999-client-1

# /data/project/fate
flow data upload -c fateflow/examples/upload/upload_guest.json


# in host 
docker exec -it confs-9999-client-1

# /data/project/fate
flow data upload -c fateflow/examples/upload/upload_host.json

# use data upload-history to see the data you upload 
```
### Job submit
#### hetero_sbt
```bash
# in /data/project/fate/example/dsl/v2/hetero_secureboost
cd /data/project/fate/example/dsl/v2/hetero_secureboost
flow job submit -c test_secureboost_train_binary_conf.json -d test_secureboost_train_dsl.json
```
#### hetero_nn
```bash
# in /data/project/fate/example/dsl/v2/hetero_nn
cd /data/project/fate/example/dsl/v2/hetero_nn
flow job submit -c test_hetero_nn_binary_conf.json -d test_hetero_nn_dsl.json
```
## Job submit with oen hundred times data 
### generate one hundred times data and upload
```bash
# confs-{party-id}-client-1

# in guest
docker exec -it confs-9999-client-1

# /data/project/fate
mkdir /example/generate
cd /example/generate

# put generate_fake_data.py in this directory
python generate_fake_data.py breast_hetero_guest.csv 100

# generate the upload josn file
cat > upload_guest.json <<EOF
{
  "file": "breast_hetero_guest.csv",
  "id_delimiter": ",",
  "head": 1,
  "partition": 4,
  "namespace": "experiment",
  "table_name": "breast_hetero_host"
}
EOF

# upload data like above in host
```
### Job submit
#### hetero_sbt
```bash
# in /data/project/fate/example/dsl/v2/hetero_secureboost
cd /data/project/fate/example/dsl/v2/hetero_secureboost
flow job submit -c test_secureboost_train_binary_conf.json -d test_secureboost_train_dsl.json
```
#### hetero_nn
```bash
# in /data/project/fate/example/dsl/v2/hetero_nn
cd /data/project/fate/example/dsl/v2/hetero_nn
flow job submit -c test_hetero_nn_binary_conf.json -d test_hetero_nn_dsl.json
```