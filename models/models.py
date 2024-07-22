from flask_sqlalchemy import SQLAlchemy
from .extensions import db

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class ResourceType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<ResourceType %r>' % self.name

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    resource_type_id = db.Column(db.Integer, db.ForeignKey('resource_type.id'))
    resource_type = db.relationship('ResourceType', backref=db.backref('resources', lazy=True))
    booked_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    booked_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Resource %r>' % self.name

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))
    resource = db.relationship('Resource', backref=db.backref('bookings', lazy=True))
    booked_at = db.Column(db.DateTime, nullable=False)
    released_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Booking %r>' % self.id