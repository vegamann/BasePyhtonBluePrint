from src.commands.get_routes import GetRoutes
from src.commands.create_route import CreateRoute
from src.session import Session, engine
from src.models.model import Base
from src.models.route import Route
from src.errors.errors import InvalidParams
from datetime import datetime, timedelta

class TestGetRoute():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

    self.data = {
      'sourceAirportCode': 'LAX',
      'sourceCountry': 'USA',
      'destinyAirportCode': 'BOG',
      'destinyCountry': 'CO',
      'bagCost': 100
    }
    self.route = CreateRoute(self.data).execute()
  
  def test_get_routes(self):
    routes = GetRoutes({
      'from': self.data['sourceAirportCode'],
      'to': self.data['destinyAirportCode'],
      'when': datetime.now().date().isoformat()
    }).execute()

    assert len(routes) == 1
    assert routes[0]['id'] == self.route['id']

    routes = GetRoutes({
      'from': self.data['destinyAirportCode'],
      'to': self.data['sourceAirportCode'],
      'when': datetime.now().date().isoformat()
    }).execute()
    assert len(routes) == 0

  def test_get_routes_invalid_when(self):
    try:
      GetRoutes({
        'from': self.data['sourceAirportCode'],
        'to': self.data['destinyAirportCode'],
        'when': 'invalid date'
      }).execute()

      assert False
    except InvalidParams:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)