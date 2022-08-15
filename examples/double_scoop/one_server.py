# Auto generated, complete the functions below

from google.protobuf.timestamp_pb2 import *
from google.protobuf.empty_pb2 import *
from two_pb2 import *
from one_pb2 import *
from yql.common import get_timestamp

class Scooper_Servicer(object):
  def Hello(_OneMessage: OneMessage) -> OneMessage:
    return OneMessage(
      name = _OneMessage.name,
      now = get_timestamp()
    )

  def WhatTime(_google_protobuf_Empty: Empty) -> Timestamp:
    # return get_timestamp()
    raise NotImplementedError

  def DoubleHello(_OneMessage: OneMessage) -> DoubleMessage:
    return DoubleMessage(
      name = _OneMessage.name * 2
    )
