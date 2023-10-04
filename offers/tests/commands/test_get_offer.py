from src.commands.create_offer import CreateOffer
from src.commands.get_offer import GetOffer
from src.session import Session, engine
from src.models.model import Base
from src.models.offer import Offer
from src.errors.errors import InvalidParam, OfferNotFoundError
from datetime import datetime, timedelta

class TestGetOffer():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    self.userId = 1
    self.data = {
      'postId': 1,
      'description': 'My description',
      'size': 'LARGE',
      'fragile': True,
      'offer': 10
    }
    self.offer = CreateOffer(self.data, self.userId).execute()

  def test_get_offer(self):
    offer = GetOffer(self.offer['id']).execute()
    assert 'id' in offer
    assert 'createdAt' in offer
    assert offer['postId'] == self.offer['postId']
    assert offer['userId'] == self.offer['userId']
    assert offer['description'] == self.offer['description']
    assert offer['size'] == self.offer['size']
    assert offer['fragile'] == self.offer['fragile']
    assert offer['offer'] == self.offer['offer']

  def test_get_offer_invalid_id(self):
    try:
      GetOffer('invalid').execute()
      assert False
    except InvalidParam:
      assert True

    print('')

  def test_get_offer_doesnt_exist(self):
    try:
      GetOffer(self.offer['id'] + 1).execute()
      assert False
    except OfferNotFoundError:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)