from .base_command import BaseCommannd
from ..models.offer import Offer, OfferSchema
from ..session import Session
from ..errors.errors import InvalidParam, OfferNotFoundError
from datetime import datetime

class GetOffer(BaseCommannd):
  def __init__(self, offer_id):
    if self.is_integer(offer_id):
      self.offer_id = int(offer_id)
    elif self.is_float(offer_id):
      self.offer_id = int(float(offer_id))
    else:
      raise InvalidParam()

  def execute(self):
    session = Session()
    if len(session.query(Offer).filter_by(id=self.offer_id).all()) <= 0:
      session.close()
      raise OfferNotFoundError()

    offer = session.query(Offer).filter_by(id=self.offer_id).one()
    schema = OfferSchema()
    offer = schema.dump(offer)
    session.close()
    return offer

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