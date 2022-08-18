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

### upload data

**python  script**

```python
from pipeline.backend.pipeline import PipeLine
pipeline_upload = PipeLine().set_initiator(role='guest', party_id=9999).set_roles(guest=9999)
partition = 4
dense_data_guest = {"name": "breast_hetero_guest", "namespace": f"experiment"}
dense_data_host = {"name": "breast_hetero_host", "namespace": f"experiment"}
tag_data = {"name": "breast_hetero_host", "namespace": f"experiment"}
import os
data_base="/data/projects/fate"
pipeline_upload.add_upload_data(file=os.path.join(data_base, "examples/data/breast_hetero_guest.csv"),
                                table_name=dense_data_guest["name"],             # table name
                                namespace=dense_data_guest["namespace"],         # namespace
                                head=1, partition=partition)               # data info

pipeline_upload.add_upload_data(file=os.path.join(data_base, "examples/data/breast_hetero_host.csv"),
                                table_name=dense_data_host["name"],
                                namespace=dense_data_host["namespace"],
                                head=1, partition=partition)

pipeline_upload.add_upload_data(file=os.path.join(data_base, "examples/data/breast_hetero_host.csv"),
                                table_name=tag_data["name"],
                                namespace=tag_data["namespace"],
                                head=1, partition=partition)
pipeline_upload.upload(drop=1)
```

### run HeteroSecureBoost

**python**

```python
from pipeline.backend.pipeline import PipeLine
from pipeline.component import Reader, DataTransform, Intersection, HeteroSecureBoost, Evaluation
from pipeline.interface import Data
pipeline = PipeLine() \
        .set_initiator(role='guest', party_id=9999) \
        .set_roles(guest=9999, host=10000)
        reader_0 = Reader(name="reader_0")
# set guest parameter
reader_0.get_party_instance(role='guest', party_id=9999).component_param(
    table={"name": "breast_hetero_guest", "namespace": "experiment"})
# set host parameter
reader_0.get_party_instance(role='host', party_id=10000).component_param(
    table={"name": "breast_hetero_host", "namespace": "experiment"})
data_transform_0 = DataTransform(name="data_transform_0")
# set guest parameter
data_transform_0.get_party_instance(role='guest', party_id=9999).component_param(
    with_label=True)
data_transform_0.get_party_instance(role='host', party_id=[10000]).component_param(
    with_label=False)
intersect_0 = Intersection(name="intersect_0")
hetero_secureboost_0 = HeteroSecureBoost(name="hetero_secureboost_0",
                                         num_trees=5,
                                         bin_num=16,
                                         task_type="classification",
                                         objective_param={"objective": "cross_entropy"},
                                         encrypt_param={"method": "paillier"},
                                         tree_param={"max_depth": 3})
evaluation_0 = Evaluation(name="evaluation_0", eval_type="binary")
pipeline.add_component(reader_0)
pipeline.add_component(data_transform_0, data=Data(data=reader_0.output.data))
pipeline.add_component(intersect_0, data=Data(data=data_transform_0.output.data))
pipeline.add_component(hetero_secureboost_0, data=Data(train_data=intersect_0.output.data))
pipeline.add_component(evaluation_0, data=Data(data=hetero_secureboost_0.output.data))
pipeline.compile()
pipeline.fit()
pipeline.dump("pipeline_saved.pkl");
pipeline = PipeLine.load_model_from_file('pipeline_saved.pkl')
pipeline.deploy_component([pipeline.data_transform_0, pipeline.intersect_0, pipeline.hetero_secureboost_0]);
reader_1 = Reader(name="reader_1")
reader_1.get_party_instance(role="guest", party_id=9999).component_param(table={"name": "breast_hetero_guest", "namespace": "experiment"})
reader_1.get_party_instance(role="host", party_id=10000).component_param(table={"name": "breast_hetero_host", "namespace": "experiment"})
evaluation_0 = Evaluation(name="evaluation_0", eval_type="binary")
predict_pipeline = PipeLine()
predict_pipeline.add_component(reader_1)\
                .add_component(pipeline, 
                               data=Data(predict_input={pipeline.data_transform_0.input.data: reader_1.output.data}))\
                .add_component(evaluation_0, data=Data(data=pipeline.hetero_secureboost_0.output.data));
predict_pipeline.predict()
```

