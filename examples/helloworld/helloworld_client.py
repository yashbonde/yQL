# Auto generated file. DO NOT EDIT.

import requests
from functools import partial

from helloworld_pb2 import HelloReply, HelloRequest

from yql.rest_pb2 import Echo
from yql.common import *


# ------ Stub ------ #

class Greeter_Stub:
  def __init__(self, url: str, session: requests.Session = None):
    self.url = url
    self.session = session or requests.Session()
    self.status = partial(call_rpc, sess = self.session, url = f"{url}/")
    self.protos = partial(call_rpc, sess = self.session, url = f"{url}/protos")

  def SayHello(self, _helloworld_HelloRequest: HelloRequest) -> HelloReply:
    """SayHello file from one location to another location"""
    echo_resp: Echo = call_rpc(
      self.session,
      f"{self.url}/predict",
      Echo(message = "HelloRequest", base64_string=message_to_b64(_helloworld_HelloRequest), rpc_name = "SayHello")
    )

    if echo_resp.base64_string == "":
      # something else happened and we don't have a proto_data, so print the message
      print("\n> Server side error:")
      for l in echo_resp.message.splitlines():
        print(l)
      print("\n")
      return None
    
    _helloworld_HelloReply = HelloReply() # predefine the output proto
    _helloworld_HelloReply = b64_to_message(echo_resp.base64_string, _helloworld_HelloReply)
    return _helloworld_HelloReply


# ------ End Stub ------ #