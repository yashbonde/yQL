from json import loads
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

import helloworld_server as server_fns

from yql.rest_pb2 import Echo
from yql.common import default_echo, message_to_dict, run_rpc, dict_to_message, message_to_json

# ------

app = FastAPI()

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
    proto_data=", ".join(server_fns.protos)
  ))
  response.status_code = 200
  return message_to_dict(echo_protos)

@app.post("/predict", response_class=JSONResponse)
async def predict(request: Request, response: Response):
  req = await request.body()
  req = req.decode()
  echo: Echo = default_echo()
  try:
    echo_req: Echo = dict_to_message(loads(req), Echo())
  except Exception as e:
    echo.message = "Invalid request: " + str(e)
    response.status_code = 400
    return message_to_dict(echo)

  # get filled protobuf
  proto_cls = server_fns.protos.get(echo_req.message, None)
  if proto_cls is None:
    echo.message = f"Invalid proto type: '{echo_req.message}'"
    response.status_code = 400
    return message_to_dict(echo)
  try:
    proto = dict_to_message(loads(echo_req.proto_data), proto_cls())
  except Exception as e:
    echo.message = "Invalid proto_data: " + str(e)
    response.status_code = 400
    return message_to_dict(echo)

  # get the rpc function to be called
  rpc_fn = server_fns.services.get(echo_req.rpc_name, None)
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

  echo.message = "OK"
  echo.proto_data = message_to_json(out)
  response.status_code = 200
  return message_to_dict(echo)
