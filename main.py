from app import app, db
from app.models import *
from app.api.routes import api
from app.auth.routes import auth


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
  app.register_blueprint(auth)
  app.run()