# Auto generated, complete the functions below

from helloworld_pb2 import *

class Greeter_Servicer(object):
  def SayHello(_helloworld_HelloRequest: HelloRequest) -> HelloReply:
    # raise NotImplementedError
    return HelloReply(
      message="Hello, " + _helloworld_HelloRequest.name
    )
