# yQL

Compile [Protobuf](https://developers.google.com/protocol-buffers/docs/proto3) to [fastAPI](https://fastapi.tiangolo.com/).

Import `{name}_client` in your application:

```python
# Client application code
from helloworld_client import GreeterStub
from helloworld_pb2 import HelloRequest, HelloReply
greeter = GreeterStub("http://127.0.0.1:8000") # define the endpoint

reply: HelloReply = greeter.SayHello(HelloRequest()) # call it by passing protobufs
print(reply.message)
```

And implement the server functions in `{name}_server.py`:

```python
... # imports

def SayHello(_helloworld_HelloRequest: HelloRequest) -> HelloReply:
  # add your code here
  raise NotImplementedError

... # other things
```

## Installation

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

