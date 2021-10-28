from app import app, db
from app.models import *


@app.shell_context_processor
def make_shell_context():
  return {
    'db': db,
    'User': User,
    'Post': Post,
    'Category': Category,
    'Comment': Comment,
    'Reply': Reply,
    'PostReaction': PostReaction,
    'CommentReaction': CommentReaction,
    'ReplyReaction': ReplyReaction
  }


if __name__ == "__main__":
  app.run()