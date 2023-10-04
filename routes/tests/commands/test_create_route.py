from src.commands.create_route import CreateRoute
from src.session import Session, engine
from src.models.model import Base
from src.models.route import Route
from src.errors.errors import IncompleteParams, RouteAlreadyExists
from datetime import datetime, timedelta

class TestCreateRoute():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_route(self):
    data = {
      'sourceAirportCode': 'LAX',
      'sourceCountry': 'USA',
      'destinyAirportCode': 'BOG',
      'destinyCountry': 'CO',
      'bagCost': 100
    }
    route = CreateRoute(data).execute()

    assert route['sourceAirportCode'] == data['sourceAirportCode']
    assert route['sourceCountry'] == data['sourceCountry']
    assert route['destinyAirportCode'] == data['destinyAirportCode']
    assert route['destinyCountry'] == data['destinyCountry']
    assert route['bagCost'] == data['bagCost']

  def test_create_route_missing_fields(self):
    data = {
      'sourceAirportCode': 'LAX',
    }
    try:
      route = CreateRoute(data).execute()
      assert False
    except IncompleteParams:
      assert len(self.session.query(Route).all()) == 0
      assert True

  def test_create_route_already_exist(self):
    data = {
      'sourceAirportCode': 'LAX',
      'sourceCountry': 'USA',
      'destinyAirportCode': 'BOG',
      'destinyCountry': 'CO',
      'bagCost': 100
    }
    CreateRoute(data).execute()

    try:
      route = CreateRoute(data).execute()
      assert False
    except RouteAlreadyExists:
      assert len(self.session.query(Route).all()) == 1
      assert True

  def test_create_route_is_expired(self):
    data = {
      'sourceAirportCode': 'LAX',
      'sourceCountry': 'USA',
      'destinyAirportCode': 'BOG',
      'destinyCountry': 'CO',
      'bagCost': 100
    }
    route = CreateRoute(data).execute()
    queried_route = self.session.query(Route).filter_by(id=route['id']).one()
    queried_route.createdAt = datetime.now() - timedelta(days=40)
    self.session.commit()

    route = CreateRoute(data).execute()

    assert len(self.session.query(Route).all()) == 2
    assert route['sourceAirportCode'] == data['sourceAirportCode']
    assert route['sourceCountry'] == data['sourceCountry']
    assert route['destinyAirportCode'] == data['destinyAirportCode']
    assert route['destinyCountry'] == data['destinyCountry']
    assert route['bagCost'] == data['bagCost']

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)