from bylog import db

class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('diary_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    private = db.Column(db.String(200), nullable=False, server_default='공개')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diary_id = db.Column(db.Integer, db.ForeignKey('diary.id', ondelete='CASCADE'))
    diary = db.relationship('Diary', backref=db.backref('comment_set',cascade='all,delete-orphan'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set'))
    user_name = db.Column(db.String(150), unique=False, nullable=False, server_default='고병용')
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=False, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    private_key = db.Column(db.String(120), unique=True, nullable=False)
    introduction = db.Column(db.String(120), nullable=True)

class Guest_book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('guest_set'))
    blog = db.Column(db.Integer, nullable=False, server_default='1')
    user_name = db.Column(db.String(150), unique=False, nullable=False, server_default='고병용')