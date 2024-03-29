from json import loads
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from one_server import Scooper_Servicer
from google.protobuf.timestamp_pb2 import *
from google.protobuf.empty_pb2 import *
from two_pb2 import *
from one_pb2 import *

proto_services = { 
  "DoubleHello": Scooper_Servicer.DoubleHello,
  "Hello": Scooper_Servicer.Hello,
  "WhatTime": Scooper_Servicer.WhatTime,
}
proto_messages = { 
  "DoubleMessage": DoubleMessage,
  "Empty": Empty,
  "OneMessage": OneMessage,
  "Timestamp": Timestamp,
}


from yql.rest_pb2 import Echo
from yql.common import *

# ------

def _fill_pb(echo_req: Echo, echo: Echo, response, decode = "b64", json_data = None) -> Echo:
  # get filled protobuf
  proto_cls = proto_messages.get(echo_req.message, None)
  if proto_cls is None:
    echo.message = f"Invalid proto type: '{echo_req.message}'"
    response.status_code = 400
    return message_to_dict(echo)
  
  echo.server_time.CopyFrom(get_timestamp())
  echo.message = echo_req.message
  try:
    if decode == "b64":
      proto = b64_to_message(echo_req.base64_string, proto_cls())
    elif decode == "json":
      proto = dict_to_message(json_data, proto_cls())
  except Exception as e:
    echo.message = "Invalid proto_data: " + str(e)
    response.status_code = 400
    return message_to_dict(echo)
  return proto

def _call_rpc(echo_req: Echo, echo: Echo, response, proto):
  # get the rpc function to be called
  rpc_fn = proto_services.get(echo_req.rpc_name, None)
  if rpc_fn is None:
    echo.message = f"Invalid rpc name: '{echo_req.rpc_name}'"
    response.status_code = 400
    return message_to_dict(echo)

  # get output and return the information
  out = run_rpc(rpc_fn, proto)
  if isinstance(out, str):
    echo.message = out
    response.status_code = 400
    return message_to_dict(echo)
  return out


async def predict(request: Request, response: Response):
  echo: Echo = default_echo()
  req = await request.body()
  req = req.decode()
  
  try:
    echo_req: Echo = dict_to_message(loads(req), Echo())
  except Exception as e:
    echo.message = "Invalid request: " + str(e)
    response.status_code = 400
    return message_to_dict(echo)

  proto = _fill_pb(echo_req, echo, response, decode = "b64")
  if isinstance(proto, dict):
    return proto

  out = _call_rpc(echo_req, echo, response, proto)
  if isinstance(out, dict):
    return out

  echo.message = "OK"
  echo.base64_string = message_to_b64(out)
  response.status_code = 200
  return message_to_dict(echo)


async def predict_json(request: Request, response: Response):
  echo: Echo = default_echo()
  req = await request.body()
  req = req.decode()

  # req has structure similar to Echo:
  # {
  #   "rpc_name": "...",
  #   "message": "...",
  #   "data": "json-data of the protobuf, client responsibility"
  # }

  try:
    json_data = loads(req)
  except Exception as e:
    echo.message = "Invalid request: " + str(e)
    response.status_code = 400
    return message_to_dict(echo)

  echo_req = Echo(rpc_name=json_data["rpc_name"], message=json_data["message"])
  proto = _fill_pb(echo_req, echo, response, decode = "json", json_data = json_data["data"])
  if isinstance(proto, dict):
    return proto

  out = _call_rpc(echo_req, echo, response, proto)
  if isinstance(out, dict):
    return out
  return message_to_dict(out)


# Define the Server
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Now add all the endpoints defined by the proto

app.add_api_route("/DoubleHello", predict, methods=["POST"], response_class=JSONResponse)
app.add_api_route("/DoubleHello_json", predict_json, methods=["POST"], response_class=JSONResponse)
app.add_api_route("/Hello", predict, methods=["POST"], response_class=JSONResponse)
app.add_api_route("/Hello_json", predict_json, methods=["POST"], response_class=JSONResponse)
app.add_api_route("/WhatTime", predict, methods=["POST"], response_class=JSONResponse)
app.add_api_route("/WhatTime_json", predict_json, methods=["POST"], response_class=JSONResponse)

# Now add default endpoints
@app.post("/", response_class=JSONResponse)
async def ping(request: Request, response: Response):
  """Echo Server"""
  # request.json
  req = await request.body()
  req = req.decode()
  echo: Echo = default_echo()
  try:
    if req:
      echo_req: Echo = dict_to_message(loads(req), Echo())
    else:
      echo_req = None
  except Exception as e:
    echo.message = "Invalid request: " + str(e)
    response.status_code = 400
  else:
    if echo_req != None:
      echo.message = echo_req.message
    response.status_code = 200
  return message_to_dict(echo)

@app.post("/protos", response_class=JSONResponse)
async def protos(request: Request, response: Response):
  """Ignores Request"""
  echo_protos: Echo = default_echo()
  echo_protos.MergeFrom(Echo(
    message="available protos",
    proto_data=", ".join(tuple(proto_messages.keys()))
  ))
  response.status_code = 200
  return message_to_dict(echo_protos)