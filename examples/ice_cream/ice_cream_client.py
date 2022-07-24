# Auto generated file. DO NOT EDIT.

import requests
from functools import partial

from ice_cream_pb2 import *

from yql.rest_pb2 import Echo
from yql.common import *


# ------ Stub ------ #

class IceCreamShop_Stub:
  def __init__(self, url: str, session: requests.Session = None):
    self.url = url.rstrip("/")
    self.session = session or requests.Session()
    self.status = partial(call_rpc, sess = self.session, url = f"{url}/")
    self.protos = partial(call_rpc, sess = self.session, url = f"{url}/protos")

  def GetIceCream(self, _IceCreamRequest: IceCreamRequest) -> IceCream:
    echo_resp: Echo = call_rpc(
      self.session,
      f"{self.url}/GetIceCream",
      Echo(message = "IceCreamRequest", base64_string=message_to_b64(_IceCreamRequest), rpc_name = "GetIceCream")
    )

    if echo_resp.base64_string == "":
      # something else happened and we don't have a proto_data, so print the message
      print("\n> Server side error:")
      for l in echo_resp.message.splitlines():
        print(l)
      print("\n")
      return None
    
    _IceCream = IceCream() # predefine the output proto
    _IceCream = b64_to_message(echo_resp.base64_string, _IceCream)
    return _IceCream

  def ThrowIceCream(self, _IceCream: IceCream) -> TissuePaper:
    echo_resp: Echo = call_rpc(
      self.session,
      f"{self.url}/ThrowIceCream",
      Echo(message = "IceCream", base64_string=message_to_b64(_IceCream), rpc_name = "ThrowIceCream")
    )

    if echo_resp.base64_string == "":
      # something else happened and we don't have a proto_data, so print the message
      print("\n> Server side error:")
      for l in echo_resp.message.splitlines():
        print(l)
      print("\n")
      return None
    
    _TissuePaper = TissuePaper() # predefine the output proto
    _TissuePaper = b64_to_message(echo_resp.base64_string, _TissuePaper)
    return _TissuePaper


# ------ End Stub ------ #