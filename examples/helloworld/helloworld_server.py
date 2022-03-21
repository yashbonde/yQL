# Auto generated, complete the functions below

import random

from helloworld_pb2 import HelloRequest, HelloReply
from yql.common import get_timestamp


def SayHello(_helloworld_HelloRequest: HelloRequest) -> HelloReply:
  raise NotImplementedError


# defined for convinience
services = { 
  "SayHello": SayHello,
}
protos = { 
  "HelloRequest": HelloRequest,
  "HelloReply": HelloReply,
}