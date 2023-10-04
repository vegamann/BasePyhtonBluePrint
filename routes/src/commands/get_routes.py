from .base_command import BaseCommannd
from ..models.route import Route, RouteSchema
from ..session import Session
from datetime import datetime, timedelta
from ..errors.errors import InvalidParams

class GetRoutes(BaseCommannd):
  def __init__(self, data):
    try:
      self.p_from = data['from'] if 'from' in data else None
      self.p_to = data['to'] if 'to' in data else None
      self.p_when = datetime.strptime(data['when'], "%Y-%m-%d") if 'when' in data else None
    except ValueError:
      raise InvalidParams
  
  def execute(self):
    session = Session()
    routes = session.query(Route).all()

    if self.p_from != None:
      routes = [route for route in routes if route.sourceAirportCode == self.p_from]

    if self.p_to != None:
      routes = [route for route in routes if route.destinyAirportCode == self.p_to]

    if self.p_when != None:
      routes = [route for route in routes if route.createdAt >= (datetime.now() - timedelta(days=30))]

    routes = RouteSchema(many=True).dump(routes)
    session.close()
    return routes