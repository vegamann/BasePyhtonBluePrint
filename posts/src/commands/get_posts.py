from .base_command import BaseCommannd
from ..models.post import Post, PostSchema
from ..session import Session
from ..errors.errors import InvalidParams
from datetime import datetime

class GetPosts(BaseCommannd):
  def __init__(self, data, userId = None):
    try:
      self.when = datetime.strptime(data['when'], "%Y-%m-%d") if 'when' in data else None
      self.routeId = data['route'] if 'route' in data else None
      self.filter = data['filter'] if 'filter' in data else None
      self.userId = userId
    except ValueError:
      raise InvalidParams()

  def execute(self):
    session = Session()
    posts = session.query(Post).all()

    if self.filter == 'me':
      posts = [post for post in posts if post.userId == int(self.userId)]

    if self.routeId != None:
      posts = [post for post in posts if post.routeId == int(self.routeId)]

    if self.when != None:
      posts = [post for post in posts if post.plannedStartDate.date().isoformat() == self.when.date().isoformat()]

    posts = PostSchema(many=True).dump(posts)
    session.close()

    return posts