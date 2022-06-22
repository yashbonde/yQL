# Auto generated file. DO NOT EDIT.

import requests
from json import loads
from functools import partial

from mongo_rpc_pb2 import MongoRequest, MongoResponse

from yql.rest_pb2 import Echo
from yql.common import call_rpc, dict_to_message, message_to_json


# ------ Stub ------ #

class MongoJsonRPCStub:
  def __init__(self, url: str, session: requests.Session = None):
    self.url = url
    self.session = session or requests.Session()
    self.status = partial(call_rpc, sess = self.session, url = f"{url}/")
    self.protos = partial(call_rpc, sess = self.session, url = f"{url}/protos")

  def Call(self, _MongoRequest: MongoRequest) -> MongoResponse:
    """Call file from one location to another location"""
    echo_resp: Echo = call_rpc(
      self.session,
      f"{self.url}/predict",
      Echo(message = "MongoRequest", proto_data = message_to_json(_MongoRequest), rpc_name = "Call")
    )
    _MongoResponse = dict_to_message(loads(echo_resp.proto_data), MongoResponse())
    return _MongoResponse

# ------ End Stub ------ #