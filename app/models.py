from flask.sessions import NullSession
from app import db
from datetime import datetime


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), nullable=False)
  surname = db.Column(db.String(64), nullable=False)
  email = db.Column(db.String(128), unique=True, nullable=False)
  password = db.Column(db.String(256), nullable=False)
  auth = db.Column(db.Boolean, default=False)

  avatar = db.Column(db.String(512), default='https://avatarfiles.alphacoders.com/498/49849.png',nullable=True)
  date_of_birth = db.Column(db.DateTime, nullable=True)
  location = db.Column(db.String(128), nullable=True)

  def __repr__(self):
    return f'id: {self.id}, name: {self.name}'


class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(128), nullable=False)
  body = db.Column(db.Text, nullable=False)
  timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
    nullable=False)
  category = db.relationship('Category',
    backref=db.backref('posts', lazy=True))
  author = db.relationship('User',
    backref=db.backref('posts', lazy=True))
  
  def __repr__(self):
    return f'id: {self.id}, title: {self.title}'


#? Post categories , e.g: Text, URL, Video
class Category(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), nullable=False)

  def __repr__(self):
    return '<Category %r>' % self.name


#? Main comments under post
class Comment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.Text, nullable=False)
  timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
  
  post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  author = db.relationship('User', backref=db.backref('comments', lazy=True))
  post = db.relationship('Post', backref=db.backref('comments', lazy=True))

  def __repr__(self):
    return f'id: {self.id}, body: {self.body}'

#? Replies to comments
class Reply(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.Text, nullable=False)
  timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
  
  comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  author = db.relationship('User', backref=db.backref('replies', lazy=True))
  parent = db.relationship('Comment', backref=db.backref('replies', lazy=True))

  def __repr__(self):
    return f'id: {self.id}, body: {self.body}'


#? Reactions 

class PostReaction(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  emote = db.Column(db.String(64), nullable=False)
  timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  author = db.relationship('User', backref=db.backref('post_reactions', lazy=True))

  parent_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
  parent = db.relationship('Post', backref=db.backref('reactions', lazy=True))


class CommentReaction(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  emote = db.Column(db.String(64), nullable=False)
  timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  author = db.relationship('User', backref=db.backref('comment_reactions', lazy=True))

  parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
  parent = db.relationship('Comment', backref=db.backref('reactions', lazy=True))


class ReplyReaction(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  emote = db.Column(db.String(64), nullable=False)
  timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  author = db.relationship('User', backref=db.backref('reply_reactions', lazy=True))

  parent_id = db.Column(db.Integer, db.ForeignKey('reply.id'), nullable=True)
  parent = db.relationship('Reply', backref=db.backref('reactions', lazy=True))