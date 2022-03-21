# yQL

Compile [Protobuf](https://developers.google.com/protocol-buffers/docs/proto3) to [fastAPI](https://fastapi.tiangolo.com/).

```
git clone https://github.com/yashbonde/yQL
cd yQL
pip install -e . # make an editable install, play with it
pip install mypy-protobuf # required to generate .pyi files, do it

# to regenerate yql/rest_pb2.pyi
protoc --python_out=./ --mypy_out=./ ./yql/assets/rest.proto && mv ./yql/assets/*.py* ./yql
```

To generate the target:
```
protoc --python_out=./ --mypy_out=./ --plugin=protoc-gen-custom=./yql/main.py --custom_out=./examples/gen ./examples/protos/helloworld.proto

cd examples/helloworld

tree -F -L 1

./
├── helloworld.proto
├── helloworld_client.py
├── helloworld_pb2.py
├── helloworld_pb2.pyi
├── helloworld_server.py
└── server.py
```

