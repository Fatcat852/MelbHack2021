from Fitnet import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    user_name = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=30), nullable=False, unique=True)
    password = db.Column(db.String(length=30), nullable=False)
    post = db.relationship('Post', backref='author', lazy='dynamic')
    # followers = db.relationship()
    followed = db.relationship('Users', secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    #like
    liked = db.relationship(
        'PostLike',
        foreign_keys='PostLike.user_id',
        backref='users', lazy='dynamic')

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0


class PostLike(db.Model):
    # __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=60), nullable=False)
    duration = db.Column(db.Integer(), nullable=False)
    type = db.Column(db.String(length=60), nullable=False)
    exercises = db.Column(db.String(), nullable=False)
    equipment = db.Column(db.String())
    author_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')

    def author(self):
        Users.query.fiter_by(id=self.author_id).name()
