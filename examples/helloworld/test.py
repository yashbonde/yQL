from helloworld_client import *

# out = message_to_string(HelloRequest(name = "lohar"))
# print(out)

stub = Greeter_Stub(
  "http://127.0.0.1:8080"
)
# print(stub.status())
# print(stub.protos())

out = stub.SayHello(HelloRequest(name = "lohar"))
print(out)

import requests

r = requests.post(
  "http://127.0.0.1:8080/SayHello_json",
  json = {
    "message": "HelloRequest",
    "rpc_name": "SayHello",
    "data": {
      "name": "lohar"
    }
  }
)
print(r.json())

# from yql.common import *
  
# x = HelloRequest(name = "lohar")
# _b64 = message_to_b64(x)
# print(_b64)

# y = b64_to_message(_b64, HelloRequest())
# print(y)

