from .base_command import BaseCommannd
from ..models.route import Route, RouteSchema
from ..session import Session
from ..errors.errors import IncompleteParams, RouteAlreadyExists
from datetime import datetime, timedelta

class CreateRoute(BaseCommannd):
  def __init__(self, data):
    self.data = data
  
  def execute(self):
    try:
      posted_route = RouteSchema(
        only=(
          'sourceAirportCode', 'sourceCountry', 'destinyAirportCode',
          'destinyCountry', 'bagCost'
        )
      ).load(self.data)
      route = Route(**posted_route)
      session = Session()

      if self.active_route_exists(session):
        session.close()
        raise RouteAlreadyExists()

      session.add(route)
      session.commit()

      new_route = RouteSchema().dump(route)
      session.close()

      return new_route
    except TypeError:
      raise IncompleteParams()

  def active_route_exists(self, session):
    existing_routes = session.query(Route).filter_by(
      sourceAirportCode=self.data['sourceAirportCode'],
      sourceCountry=self.data['sourceCountry'],
      destinyAirportCode=self.data['destinyAirportCode'],
      destinyCountry=self.data['destinyCountry'],
    ).all()
    existing_routes = [route for route in existing_routes if route.createdAt >= (datetime.now() - timedelta(days=30))]

    return len(existing_routes) > 0