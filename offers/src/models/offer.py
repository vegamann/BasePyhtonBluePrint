from marshmallow import  Schema, fields
from sqlalchemy import Column, Integer, Integer, String, Boolean
from .model import Model, Base

class Offer(Model, Base):
  __tablename__ = 'offers'
  
  postId = Column(Integer)
  userId = Column(Integer)
  description = Column(String)
  size = Column(String)
  fragile = Column(Boolean)
  offer = Column(Integer)

  def __init__(
    self, postId, userId,
    description, size, fragile,
    offer
  ):
    Model.__init__(self)
    self.postId = postId
    self.userId = userId
    self.description = description
    self.size = size
    self.fragile = fragile
    self.offer = offer

class OfferSchema(Schema):
  id = fields.Number()
  postId = fields.Number()
  userId = fields.Number()
  description = fields.Str()
  size = fields.Str()
  fragile = fields.Bool()
  offer = fields.Number()
  createdAt = fields.DateTime()