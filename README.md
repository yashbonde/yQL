# yQL

Compile [Protobuf](https://developers.google.com/protocol-buffers/docs/proto3) to [fastAPI](https://fastapi.tiangolo.com/), embeds `yql` in generated folder so you don't have to install it.

Used in production at [NimbleBox](http://nimblebox.ai/).

## Usage

Install `protoc` on your machine:

```
protoc --python_out=./ --mypy_out=./ --plugin=protoc-gen-custom=./yql/main.py --custom_out=./examples/gen ./examples/protos/helloworld.proto
```

This will create the following files:

```
./
├── helloworld.proto
├── helloworld_client.py
├── helloworld_pb2.py
├── helloworld_pb2.pyi
├── helloworld_server.py
├── server.py
└── yql/
    ├── __init__.py
    ├── common.py
    ├── rest_pb2.py
    └── rest_pb2.pyi
```

Import `{name}_client` in your application:

```python
greeter = GreeterStub("http://127.0.0.1:8000") # define the endpoint
reply: HelloReply = greeter.SayHello(HelloRequest()) # call it by passing protobufs
print(reply.message)
```

And implement the server functions in `{name}_server.py`:

```python
class Greeter_Servicer(object):
  def SayHello(_helloworld_HelloRequest: HelloRequest) -> HelloReply:
    return HelloReply(message = "Hi " + _helloworld_HelloRequest.name + "!")
```

## Installation

```
git clone https://github.com/yashbonde/yQL
cd yQL
pip install -e . # make an editable install, play with it

# to regenerate yql/rest_pb2.pyi
protoc --python_out=./ --mypy_out=./ ./yql/assets/rest.proto && mv ./yql/assets/*.py* ./yql
```
