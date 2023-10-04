from src.commands.create_post import CreatePost
from src.session import Session, engine
from src.models.model import Base
from src.models.post import Post
from src.errors.errors import IncompleteParams, InvalidDates
from datetime import datetime, timedelta

class TestCreatePost():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_post(self):
    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    post = CreatePost(data, userId).execute()

    assert post['routeId'] == data['routeId']
    assert post['userId'] == userId
    assert 'plannedStartDate' in post
    assert 'plannedEndDate' in post

  def test_create_post_missing_fields(self):
    try:
      CreatePost({}).execute()
      assert False
    except IncompleteParams:
      assert True

  def test_create_post_invalid_dates(self):
    try:
      data = {
        'routeId': 1,
        'plannedStartDate': (datetime.now() + timedelta(days=2)).date().isoformat(),
        'plannedEndDate': datetime.now().date().isoformat()
      }
      userId = 1
      CreatePost(data, userId).execute()
      assert False
    except InvalidDates:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)