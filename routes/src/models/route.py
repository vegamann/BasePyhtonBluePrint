from marshmallow import  Schema, fields
from sqlalchemy import Column, String, DateTime, Integer
from .model import Model, Base
from datetime import timedelta

class Route(Model, Base):
  __tablename__ = 'routes'

  sourceAirportCode = Column(String)
  sourceCountry = Column(String)
  destinyAirportCode = Column(String)
  destinyCountry = Column(String)
  bagCost = Column(Integer)
  expireAt = Column(DateTime)

  def __init__(
    self, sourceAirportCode, sourceCountry,
    destinyAirportCode, destinyCountry, bagCost
  ):
    Model.__init__(self)
    self.sourceAirportCode = sourceAirportCode
    self.sourceCountry = sourceCountry
    self.destinyAirportCode = destinyAirportCode
    self.destinyCountry = destinyCountry
    self.bagCost = bagCost
    self.expireAt = self.createdAt + timedelta(days=30)

class RouteSchema(Schema):
  id = fields.Number()
  sourceAirportCode = fields.Str()
  sourceCountry = fields.Str()
  destinyAirportCode = fields.Str()
  destinyCountry = fields.Str()
  bagCost = fields.Number()
  createdAt = fields.DateTime()
  expireAt = fields.DateTime()