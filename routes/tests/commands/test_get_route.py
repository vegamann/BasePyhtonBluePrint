from src.commands.get_route import GetRoute
from src.commands.create_route import CreateRoute
from src.session import Session, engine
from src.models.model import Base
from src.models.route import Route
from src.errors.errors import InvalidParams, RouteNotFoundError

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

  def test_get_route(self):
    route = GetRoute(self.route['id']).execute()

    assert route['id'] == self.route['id']
    assert route['sourceAirportCode'] == self.route['sourceAirportCode']
    assert route['sourceCountry'] == self.route['sourceCountry']
    assert route['destinyAirportCode'] == self.route['destinyAirportCode']
    assert route['destinyCountry'] == self.route['destinyCountry']
    assert route['bagCost'] == self.route['bagCost']

  def test_get_route_invalid_id(self):
    try:
      GetRoute('non_number_id').execute()

      assert False
    except InvalidParams:
      assert True

  def test_get_route_doesnt_exist(self):
    try:
      GetRoute(self.route['id'] + 1).execute()

      assert False
    except RouteNotFoundError:
      assert True

  
  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)