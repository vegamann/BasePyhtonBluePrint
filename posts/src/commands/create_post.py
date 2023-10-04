from .base_command import BaseCommannd
from ..models.post import Post, PostSchema
from ..session import Session
from ..errors.errors import IncompleteParams, InvalidDates
from datetime import datetime

class CreatePost(BaseCommannd):
  def __init__(self, data, userId = None):
    self.data = data
    if 'plannedStartDate' in data:
      self.data['plannedStartDate'] = str(datetime.strptime(data['plannedStartDate'], "%Y-%m-%d"))
    if 'plannedEndDate' in data:
      self.data['plannedEndDate'] = str(datetime.strptime(data['plannedEndDate'], "%Y-%m-%d"))
    if userId != None:
      self.data['userId'] = userId
  
  def execute(self):
    try:
      posted_post = PostSchema(
        only=('routeId', 'userId', 'plannedStartDate', 'plannedEndDate')
      ).load(self.data)
      post = Post(**posted_post)

      if not self.valid_dates():
        raise InvalidDates()

      session = Session()

      session.add(post)
      session.commit()

      new_post = PostSchema().dump(post)
      session.close()

      return new_post
    except TypeError:
      raise IncompleteParams

  def valid_dates(self):
    init = datetime.strptime(self.data['plannedStartDate'], "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(self.data['plannedEndDate'], "%Y-%m-%d %H:%M:%S")
    return init < end