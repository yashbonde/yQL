import io
import sys
import base64
import logging
import traceback
from json import loads
from inspect import signature

import requests
import random
from functools import partial
from google.protobuf.json_format import ParseDict, MessageToDict, MessageToJson
from google.protobuf.text_format import MessageToString, Parse as ParseString
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.message import Message

from .rest_pb2 import Echo

_logger = None

message_to_dict = partial(
  MessageToDict,
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
  # logger.info(f"POST {url} | json: {message}")
  r = fn(url, json = message)

  if r.status_code == 400:
    data = loads(r.text)
    out = dict_to_message(data, Echo())
    if out.base64_string == "":
      if _logger:
        _logger.error(f"400: {out.message}")
      else:
        print(f"400: {out.message}")
      return None
  elif r.status_code == 501:
    if _logger:
      _logger.error("501: NOT IMPLEMENTED")
    else:
      print("501: NOT IMPLEMENTED")
    return None
  elif r.status_code == 500:
    if _logger:
      _logger.error("500: INTERNAL SERVER ERROR")
    else:
      print("500: INTERNAL SERVER ERROR")
    return None
  out = dict_to_message(r.json(), Echo())
  return out

def run_rpc(service_fn, message, **kwargs) -> Message:
  _echo = default_echo()

  # check if correct arguments are being sent or not
  args = signature(service_fn).parameters
  if len(args) - 1 < len(kwargs):
    if _logger:
      _logger.error(f"Service function takes upto {len(args) - 1} arguments, but {len(kwargs)} were provided")
    else:
      print(f"Service function takes upto {len(args) - 1} arguments, but {len(kwargs)} were provided")
    _echo.message = "500: INTERNAL SERVER ERROR"
    return _echo

  # run it and handle any exceptions
  try:
    response = service_fn(message, **kwargs)
  except NotImplementedError:
    return Echo(server_time=get_timestamp(), message = "501: NOT IMPLEMENTED")
  except Exception as e:
    f = traceback.format_exc()
    for l in f.splitlines():
      if _logger:
        _logger.error(l)
      else:
        print(l)
    return Echo(server_time=get_timestamp(), message = "500: INTERNAL SERVER ERROR")
  
  # manage response
  if isinstance(response, str):
    _echo.message = f"400: {response}" 
    response = _echo
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

def set_logger(logger):
  global _logger
  _logger = logger
