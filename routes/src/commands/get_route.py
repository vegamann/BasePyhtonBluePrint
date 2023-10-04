from .base_command import BaseCommannd
from ..models.route import Route, RouteSchema
from ..session import Session
from ..errors.errors import InvalidParams, RouteAlreadyExists, RouteNotFoundError

class GetRoute(BaseCommannd):
  def __init__(self, route_id):
    if self.is_integer(route_id):
      self.route_id = int(route_id)
    elif self.is_float(route_id):
      self.route_id = int(float(route_id))
    else:
      raise InvalidParams()

  def execute(self):
    session = Session()
    if len(session.query(Route).filter_by(id=self.route_id).all()) <= 0:
      session.close()
      raise RouteNotFoundError()

    route = session.query(Route).filter_by(id=self.route_id).one()
    schema = RouteSchema()
    route = schema.dump(route)
    session.close()
    return route

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