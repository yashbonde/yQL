# Auto generated file. DO NOT EDIT.

import requests
from functools import partial

from google.protobuf.timestamp_pb2 import *
from google.protobuf.empty_pb2 import *
from two_pb2 import *
from one_pb2 import *

from yql.rest_pb2 import Echo
from yql.common import *


# ------ Stub ------ #

class Scooper_Stub:
  def __init__(self, url: str, session: requests.Session = None):
    self.url = url.rstrip("/")
    self.session = session or requests.Session()
    self.status = partial(call_rpc, sess = self.session, url = f"{url}/")
    self.protos = partial(call_rpc, sess = self.session, url = f"{url}/protos")

  def Hello(self, _OneMessage: OneMessage) -> OneMessage:
    echo_resp: Echo = call_rpc(
      self.session,
      f"{self.url}/Hello",
      Echo(message = "OneMessage", base64_string=message_to_b64(_OneMessage), rpc_name = "Hello")
    )

    if echo_resp.base64_string == "" and echo_resp.message != "OK":
      # something else happened and we don't have a proto_data, so print the message
      print("\n> Server side error:")
      for l in echo_resp.message.splitlines():
        print(l)
      print("\n")
      return None
    
    _OneMessage = OneMessage() # predefine the output proto
    _OneMessage = b64_to_message(echo_resp.base64_string, _OneMessage)
    return _OneMessage

  def WhatTime(self, _google_protobuf_Empty: Empty) -> Timestamp:
    echo_resp: Echo = call_rpc(
      self.session,
      f"{self.url}/WhatTime",
      Echo(message = "Empty", base64_string=message_to_b64(_google_protobuf_Empty), rpc_name = "WhatTime")
    )

    if echo_resp.base64_string == "" and echo_resp.message != "OK":
      # something else happened and we don't have a proto_data, so print the message
      print("\n> Server side error:")
      for l in echo_resp.message.splitlines():
        print(l)
      print("\n")
      return None
    
    _google_protobuf_Timestamp = Timestamp() # predefine the output proto
    _google_protobuf_Timestamp = b64_to_message(echo_resp.base64_string, _google_protobuf_Timestamp)
    return _google_protobuf_Timestamp

  def DoubleHello(self, _OneMessage: OneMessage) -> DoubleMessage:
    echo_resp: Echo = call_rpc(
      self.session,
      f"{self.url}/DoubleHello",
      Echo(message = "OneMessage", base64_string=message_to_b64(_OneMessage), rpc_name = "DoubleHello")
    )

    if echo_resp.base64_string == "" and echo_resp.message != "OK":
      # something else happened and we don't have a proto_data, so print the message
      print("\n> Server side error:")
      for l in echo_resp.message.splitlines():
        print(l)
      print("\n")
      return None
    
    _DoubleMessage = DoubleMessage() # predefine the output proto
    _DoubleMessage = b64_to_message(echo_resp.base64_string, _DoubleMessage)
    return _DoubleMessage


# ------ End Stub ------ #