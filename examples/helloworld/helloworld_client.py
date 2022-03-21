# Auto generated file. DO NOT EDIT.

import requests
from json import loads
from functools import partial


from helloworld_pb2 import HelloRequest, HelloReply
from rest_pb2 import Echo
from yql.common import call_rpc, dict_to_message, message_to_json


# ------ Stub ------ #

class GreeterStub:
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
      Echo(message = "HelloRequest", proto_data = message_to_json(_helloworld_HelloRequest), rpc_name = "SayHello")
    )
    _helloworld_HelloReply = dict_to_message(loads(echo_resp.proto_data), HelloReply())
    return _helloworld_HelloReply

# ------ End Stub ------ #