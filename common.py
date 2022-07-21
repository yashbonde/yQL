import io
import sys
import base64
import traceback
from json import loads

import requests
import random
from functools import partial
from google.protobuf.json_format import ParseDict, MessageToDict, MessageToJson
from google.protobuf.text_format import MessageToString, Parse as ParseString
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.message import Message

from .rest_pb2 import Echo

message_to_dict = partial(
  MessageToDict,
  including_default_value_fields = True,
  preserving_proto_field_name = True,
  use_integers_for_enums = True,
  float_precision = 4
)

dict_to_message = partial(
  ParseDict,
  ignore_unknown_fields = True,
)

message_to_json = partial(
  MessageToJson,
  including_default_value_fields = True,
  preserving_proto_field_name = True,
  use_integers_for_enums = True,
  float_precision = 4
)

message_to_string = partial(
  MessageToString,
  as_utf8 = False,
  as_one_line = False, # does a simple rstrip on the end
  # use_short_repeated_primitives = False,
  pointy_brackets = False,
  use_index_order = False,
  use_field_number=False,
  print_unknown_fields=True,
)

string_to_message = partial(
  ParseString,
  allow_unknown_field = True,
)

def message_to_b64(message: Message) -> str:
  return base64.b64encode(message.SerializeToString()).decode("utf-8")

def b64_to_message(b64: str, message: Message) -> Message:
  message.ParseFromString(base64.b64decode(b64))
  return message


def call_rpc(sess: requests.Session, url: str, message: Echo = None):
  fn = sess.post
  if message != None:
    message = message_to_dict(message)
  # print(f"POST {url} | json: {message}")
  r = fn(url, json = message)

  if r.status_code == 400:
    data = loads(r.text)
    out = dict_to_message(data, Echo())
    return out

  try:
    r.raise_for_status()
  except Exception as e:
    # logging.error(r.content)
    raise e
  out = dict_to_message(r.json(), Echo())
  return out

def run_rpc(service_fn, message):
  # logging.info(f"service_fn: {service_fn.__qualname__}")
  try:
    response = service_fn(message)
  except NotImplementedError:
    return default_echo()
  except Exception as e:
    f = io.StringIO("")
    traceback.print_exception(*sys.exc_info(), file = f)
    return f.getvalue()
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
