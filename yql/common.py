import requests
import random
from functools import partial
from google.protobuf.json_format import ParseDict, MessageToDict, MessageToJson
from google.protobuf.timestamp_pb2 import Timestamp

from .rest_pb2 import Echo

import logging
logging.basicConfig(level=logging.INFO)

message_to_dict = partial(
  MessageToDict,
  including_default_value_fields = False,
  preserving_proto_field_name = True,
  use_integers_for_enums = True,
  float_precision = 4
)

message_to_json = partial(
  MessageToJson,
  including_default_value_fields = False,
  preserving_proto_field_name = True,
  use_integers_for_enums = True,
  float_precision = 4
)

dict_to_message = partial(
  ParseDict,
  ignore_unknown_fields = True,
)

def call_rpc(sess: requests.Session, url: str, message: Echo = None):
  fn = sess.post
  if message != None:
    message = message_to_dict(message)
  logging.info(f"POST {url} | json: {message}")
  r = fn(url, json = message)
  try:
    r.raise_for_status()
  except Exception as e:
    logging.error(r.text)
    raise e
  out = dict_to_message(r.json(), Echo())
  return out

def run_rpc(service_fn, message):
  logging.info(f"service_fn: {service_fn.__qualname__}")
  try:
    response = service_fn(message)
  except Exception as e:
    return str(e)
  return response

def get_timestamp() -> Timestamp:
  _time = Timestamp()
  _time.GetCurrentTime()
  return _time

def default_echo() -> Echo:
  return Echo(
    server_time=get_timestamp(),
    message = "".join(random.choices("abcedfghijklmnopqrtsuvwxyz0123456789", k = 32))
  )
