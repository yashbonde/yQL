from helloworld_client import *

# out = message_to_string(HelloRequest(name = "charmi"))
# print(out)

stub = Greeter_Stub(
  "http://127.0.0.1:8000"
)
print(stub.status())
print(stub.protos())

out = stub.SayHello(HelloRequest(name = "charmi"))
print(out)

# from yql.common import *
  
# x = HelloRequest(name = "charmi")
# _b64 = message_to_b64(x)
# print(_b64)

# y = b64_to_message(_b64, HelloRequest())
# print(y)

