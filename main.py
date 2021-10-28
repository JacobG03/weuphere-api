from app import app, db
from app.models import *
from app.api.routes import api


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
  app.register_blueprint(api)
  app.run()