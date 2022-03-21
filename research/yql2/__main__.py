# from fire import Fire
# from .compiler import compiler

# https://expobrain.net/2015/09/13/create-a-plugin-for-google-protocol-buffer/
# https://golangexample.com/create-a-protocol-buffers-protobuf-plugin-which-is-executed-with-the-protoc-compile/
# https://rotemtam.com/2021/03/22/creating-a-protoc-plugin-to-gen-go-code/

import sys
from typing import Iterator, Tuple

from contextlib import contextmanager
from google.protobuf.compiler import plugin_pb2 as plugin_pb2

@contextmanager
def code_generation() -> Iterator[
    Tuple[plugin_pb2.CodeGeneratorRequest, plugin_pb2.CodeGeneratorResponse],
]:
    if len(sys.argv) > 1 and sys.argv[1] in ("-V", "--version"):
        print("yql-protobuf-compiler version 0.0.1")
        sys.exit(0)

    # Read request message from stdin
    data = sys.stdin.buffer.read()

    # Parse request
    request = plugin_pb2.CodeGeneratorRequest()
    request.ParseFromString(data)

    # Create response
    response = plugin_pb2.CodeGeneratorResponse()

    # Declare support for optional proto3 fields
    response.supported_features |= (
        plugin_pb2.CodeGeneratorResponse.FEATURE_PROTO3_OPTIONAL
    )

    yield request, response

    # Serialise response message
    output = response.SerializeToString()

    # Write to stdout
    sys.stdout.buffer.write(output)

if __name__ == "__main__":
  # Fire(compiler)
  pass
