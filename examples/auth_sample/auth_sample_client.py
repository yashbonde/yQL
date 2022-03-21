# Auto generated file. DO NOT EDIT.

import requests
from json import loads
from functools import partial


from auth_sample_pb2 import Request, Response
from rest_pb2 import Echo
from yql.common import call_rpc, dict_to_message, message_to_json


# ------ Stub ------ #

class TestServiceStub:
  def __init__(self, url: str, session: requests.Session = None):
    self.url = url
    self.session = session or requests.Session()
    self.status = partial(call_rpc, sess = self.session, url = f"{url}/")
    self.protos = partial(call_rpc, sess = self.session, url = f"{url}/protos")

  def UnaryCall(self, _grpc_testing_Request: Request) -> Response:
    """UnaryCall file from one location to another location"""
    echo_resp: Echo = call_rpc(
      self.session,
      f"{self.url}/predict",
      Echo(message = "Request", proto_data = message_to_json(_grpc_testing_Request), rpc_name = "UnaryCall")
    )
    _grpc_testing_Response = dict_to_message(loads(echo_resp.proto_data), Response())
    return _grpc_testing_Response

# ------ End Stub ------ #