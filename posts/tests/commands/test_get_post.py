from src.commands.get_post import GetPost
from src.commands.create_post import CreatePost
from src.session import Session, engine
from src.models.model import Base
from src.models.post import Post
from src.errors.errors import InvalidParams, PostNotFoundError
from datetime import datetime, timedelta

class TestGetPost():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

    data = {
      'routeId': 1,
      'plannedStartDate': datetime.now().date().isoformat(),
      'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
    }
    userId = 1
    self.post = CreatePost(data, userId).execute()

  def test_get_post(self):
    post = GetPost(self.post['id']).execute()

    assert post['id'] == self.post['id']
    assert post['userId'] == self.post['userId']
    assert post['plannedStartDate'] == self.post['plannedStartDate']
    assert post['plannedEndDate'] == self.post['plannedEndDate']

  def test_get_post_invalid_id(self):
    try:
      GetPost('Invalid').execute()
      assert False
    except InvalidParams:
      assert True

  def test_get_post_doesnt_exist(self):
    try:
      GetPost(self.post['id'] + 1).execute()
      assert False
    except PostNotFoundError:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)