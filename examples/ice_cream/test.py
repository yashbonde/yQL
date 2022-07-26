# from locust import HttpLocust, task

# class LoadTester(HttpLocust):
#   def request_icecream(self):
#     self.client.post("/", json={"message": "ping"})

from ice_cream_client import *

stub = IceCreamShop_Stub("http://127.0.0.1:8080")
out = stub.GetIceCream(IceCreamRequest(flavor=Flavor.STRAWBERRY, customer_name="yash bonde"))
print(out)

import requests

r = requests.post(
  "http://127.0.0.1:8080/GetIceCream_json",
  json = {
    "message": "IceCreamRequest",
    "rpc_name": "GetIceCream",
    "data": {
      "flavor": Flavor.STRAWBERRY,
      "customer_name": "yash bonde"
    }
  }
)

print(r.json())
