# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: examples/auth_sample/auth_sample.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&examples/auth_sample/auth_sample.proto\x12\x0cgrpc.testing\":\n\x07Request\x12\x15\n\rfill_username\x18\x04 \x01(\x08\x12\x18\n\x10\x66ill_oauth_scope\x18\x05 \x01(\x08\"1\n\x08Response\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x13\n\x0boauth_scope\x18\x03 \x01(\t2I\n\x0bTestService\x12:\n\tUnaryCall\x12\x15.grpc.testing.Request\x1a\x16.grpc.testing.ResponseB\x07\xa2\x02\x04\x41UTHb\x06proto3')



_REQUEST = DESCRIPTOR.message_types_by_name['Request']
_RESPONSE = DESCRIPTOR.message_types_by_name['Response']
Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), {
  'DESCRIPTOR' : _REQUEST,
  '__module__' : 'examples.auth_sample.auth_sample_pb2'
  # @@protoc_insertion_point(class_scope:grpc.testing.Request)
  })
_sym_db.RegisterMessage(Request)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSE,
  '__module__' : 'examples.auth_sample.auth_sample_pb2'
  # @@protoc_insertion_point(class_scope:grpc.testing.Response)
  })
_sym_db.RegisterMessage(Response)

_TESTSERVICE = DESCRIPTOR.services_by_name['TestService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\242\002\004AUTH'
  _REQUEST._serialized_start=56
  _REQUEST._serialized_end=114
  _RESPONSE._serialized_start=116
  _RESPONSE._serialized_end=165
  _TESTSERVICE._serialized_start=167
  _TESTSERVICE._serialized_end=240
# @@protoc_insertion_point(module_scope)
