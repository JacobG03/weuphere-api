from app import db
from app.models import *


"""
'db': db,
'User': User,
'Post': Post,
'Category': Category,
'Comment': Comment,
'Reply': Reply,
'PostReaction': PostReaction,
'CommentReaction': CommentReaction,
'ReplyReaction': ReplyReaction
"""


def createUsers(username, n):
  for i in range(0, n):
    user = User(username=f'{username}{i}', email=f'{username}{i}@gmail.com', password='1234')
    db.session.add(user)

  db.session.commit()
  return True


