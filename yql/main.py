#!/usr/bin/env python3
# ^^^^^^^^^^^^^^^^^^^^
# Need to define this since protoc expects the plugin to be an executable.

# https://expobrain.net/2015/09/13/create-a-plugin-for-google-protocol-buffer/
# https://golangexample.com/create-a-protocol-buffers-protobuf-plugin-which-is-executed-with-the-protoc-compile/
# https://rotemtam.com/2021/03/22/creating-a-protoc-plugin-to-gen-go-code/
# Protofile for CodeGeneratorRequest/Response https://github.com/protocolbuffers/protobuf/blob/master/src/google/protobuf/compiler/plugin.proto
# Description of SourceCodeInfo: https://github.com/protocolbuffers/protobuf/blob/master/src/google/protobuf/descriptor.proto

import os
import sys
import jinja2
from typing import Iterator, Tuple

file_x = lambda *x: os.path.join(os.path.dirname(__file__), *x)

from contextlib import contextmanager
from google.protobuf.compiler.plugin_pb2 import CodeGeneratorRequest, CodeGeneratorResponse

class Env:
  YQL_FOLDER: str = lambda x: os.getenv("YQL_FOLDER", x)
  YQL_PBREL: str = lambda x: os.getenv("YQL_PBREL", x)

@contextmanager
def code_generation() -> Iterator[Tuple[CodeGeneratorRequest, CodeGeneratorResponse]]:
    if len(sys.argv) > 1 and sys.argv[1] in ("-V", "--version"):
      print("yql-protobuf-compiler version 0.0.1")
      sys.exit(0)

    # create Protos
    request = CodeGeneratorRequest()
    response = CodeGeneratorResponse()
    response.supported_features |= (CodeGeneratorResponse.FEATURE_PROTO3_OPTIONAL)

    request.ParseFromString(sys.stdin.buffer.read())
    # with open(file_x("sample.txt"), "w") as f:
    #   f.write(repr(request.proto_file[0].name))

    yield request, response

    # iterate over all the files in the data
    for proto_file in request.proto_file:

      if len(proto_file.service) == 0:
        response.error = "No service definition found"
        sys.stdout.buffer.write(response.SerializeToString())
        return
      if len(proto_file.service) > 1:
        response.error = "Multiple service definitions found, should contain only one"
        sys.stdout.buffer.write(response.SerializeToString())
        return
      sys.stdout.buffer.write(response.SerializeToString())
      
      # create the data points
      proto_imports = {}
      all_services = set()
      all_protos = set()
      
      # create all the data needed to write the file
      # TODO: @yashbonde: figure out how to get the comments as well for the parts
      trg_folder = Env.YQL_FOLDER("")
      pb_relative = Env.YQL_PBREL("")
      if pb_relative:
        pb_relative += "."
      proto_folder, proto_name = os.path.split(proto_file.name)
      trg_folder = trg_folder or proto_folder

      run_server = os.path.join(trg_folder, "server.py")
      trg_server = os.path.join(trg_folder, proto_name.split(".")[0] + "_server.py")
      trg_client = os.path.join(trg_folder, proto_name.split(".")[0] + "_client.py")

      service = proto_file.service[0]
      service_tuples = []
      for method in service.method:
        # process the input message information
        _in_var =  method.input_type.replace(".", "_")
        _in_proto = method.input_type.strip(".")
        _in_proto_message = _in_proto.split(".")[-1]
        proto_imports.setdefault(pb_relative + proto_name.split(".")[0] + "_pb2", []).append(_in_proto_message)

        # process the output message information
        _out_var = method.output_type.replace(".", "_")
        _out_proto = method.output_type.strip(".")
        _out_proto_message = _out_proto.split(".")[-1]
        proto_imports.setdefault(pb_relative + proto_name.split(".")[0] + "_pb2", []).append(_out_proto_message)

        # create the service tuple
        service_tuples.append((method.name, _in_var, _in_proto_message, _out_var, _out_proto_message))
        all_services.add(method.name)
        all_protos.add(_in_proto_message)
        all_protos.add(_out_proto_message)
      # imports_strings = [f"from {k} import {', '.join(set(v))}" for k,v in proto_imports.items()]
      imports_strings = [f"from {k} import *" for k,v in proto_imports.items()]
      all_services = sorted(all_services)
      all_protos = sorted(all_protos)

      # load the jinja templates
      with open(file_x("assets", "server_stub.jinja"), "r") as src, open(trg_server, "w") as trg:
        trg.write(jinja2.Template(src.read()).render(
          service_tuples=service_tuples,
          imports_strings=imports_strings,
          service_name=service.name,
        ))

      with open(file_x("assets", "client_stub.jinja"), "r") as src, open(trg_client, "w") as trg:
        trg.write(jinja2.Template(src.read()).render(
          service_tuples=service_tuples,
          imports_strings=imports_strings,
          service_name = service.name,
          zip=zip
        ))

      with open(file_x("assets", "server.jinja"), "r") as src, open(run_server, "w") as trg:
        trg.write(jinja2.Template(src.read()).render(
          server_stub = proto_name.split(".")[0] + "_server",
          service_name = service.name,
          all_services=list(all_services),
          all_protos=list(all_protos),
          imports_strings=imports_strings,
        ))

      # embed yql in target folder
      files_to_move = [file_x("__init__.py"), file_x("common.py"), file_x("rest_pb2.py"), file_x("rest_pb2.pyi")]
      if not os.path.exists(f"{trg_folder}/yql"):
        os.system(f"mkdir {trg_folder}/yql")
        os.system(f"cp {' '.join(files_to_move)} {trg_folder}/yql")


def main():
  with code_generation() as (request, response):
    pass

if __name__ == "__main__":
  main()
