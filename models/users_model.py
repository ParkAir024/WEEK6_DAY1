from datetime import datetime

from app import db


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

class UsersModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(75), nullable=False, unique=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    followed = db.relationship('UsersModel',
                               secondary='followers',
                               primaryjoin=followers.c.follower_id == id,
                               secondaryjoin=followers.c.followed_id == id,
                               backref=db.backref('followers', lazy='dynamic')
                               )

    def __repr__(self):
        return f'<User: {self.username}>'

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def from_dict(self, user_dict):
        for k, v in user_dict.items():
            setattr(self, k, v)

class GameModel(db.Model):

  __tablename__ = 'games'

  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.String, nullable=False)
  timestamp = db.Column(db.DateTime, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  user = db.relationship(UsersModel, back_populates ='games')

  __table_args__ = {'extend_existing': True}

  def __repr__(self):
    return f'<Games: {self.body}>'
  
  def commit(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
