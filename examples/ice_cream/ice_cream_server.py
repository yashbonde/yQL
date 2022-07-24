# Auto generated, complete the functions below

from ice_cream_pb2 import *

class IceCreamShop_Servicer(object):
  def GetIceCream(_IceCreamRequest: IceCreamRequest) -> IceCream:
    return IceCream(
      flavor = _IceCreamRequest.flavor,
      customer_name = _IceCreamRequest.customer_name,
      finished = False
    )

  def ThrowIceCream(_IceCream: IceCream) -> TissuePaper:
    return TissuePaper(
      message = "Thankyou for chosing Naturals!"
    )
