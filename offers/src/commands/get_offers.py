from .base_command import BaseCommannd
from ..models.offer import Offer, OfferSchema
from ..session import Session
from ..errors.errors import InvalidParam, IncompleteParams
from datetime import datetime

class GetOffers(BaseCommannd):
  def __init__(self, data, userId = None):
    self.filter = data['filter'] if 'filter' in data else None
    if 'post' in data:
      if self.is_integer(str(data['post'])):
        self.postId = int(data['post'] )
      elif self.is_float(str(data['post'])):
        self.postId = int(float(data['post'] ))
      else:
        raise InvalidParam()
    else:
      self.postId = None

    if userId == None:
      raise IncompleteParams()
    else:
      self.userId = userId

  def execute(self):
    session = Session()
    offers = session.query(Offer).all()

    if self.filter == 'me':
      offers = [offer for offer in offers if offer.userId == self.userId]

    if self.postId != None:
      offers = [offer for offer in offers if offer.postId == self.postId]


    offers = OfferSchema(many=True).dump(offers)
    session.close()
    return offers

  def is_integer(self, string):
    try:
      int(string)
      return True
    except:
      return False

  def is_float(self, string):
    try:
      float(string)
      return True
    except:
      return False