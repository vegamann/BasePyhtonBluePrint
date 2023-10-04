from marshmallow import  Schema, fields
from sqlalchemy import Column, DateTime, Integer, Integer
from .model import Model, Base

class Post(Model, Base):
  __tablename__ = 'users'

  routeId = Column(Integer)
  userId = Column(Integer)
  plannedStartDate = Column(DateTime)
  plannedEndDate = Column(DateTime)

  def __init__(self, routeId, userId, plannedStartDate, plannedEndDate):
    Model.__init__(self)
    self.routeId = routeId
    self.userId = userId
    self.plannedStartDate = plannedStartDate
    self.plannedEndDate = plannedEndDate

class PostSchema(Schema):
  id = fields.Number()
  routeId = fields.Number()
  userId = fields.Number()
  plannedStartDate = fields.DateTime()
  plannedEndDate = fields.DateTime()
  createdAt = fields.DateTime()
