from models import db
from datetime import datetime
datetime.utcnow()

class ResourceType(db.Model):
    __tablename__ = 'resource_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"ResourceType('{self.name}')"

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255))
    category = db.Column(db.String(50), nullable=True)
    available = db.Column(db.Boolean, default=True)  
    available_from = db.Column(db.DateTime, default=datetime.utcnow) 
    resource_type_id = db.Column(db.Integer, db.ForeignKey('resource_type.id'))
    resource_type = db.relationship('ResourceType', backref=db.backref('resources', lazy=True))
    booked_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    booked_at = db.Column(db.DateTime, nullable=True)


    def __init__(self, **kwargs):
        if isinstance(kwargs.get('available_from'), str):
            kwargs['available_from'] = datetime.strptime(kwargs['available_from'], '%Y-%m-%d')
        if isinstance(kwargs.get('booked_at'), str):
            kwargs['booked_at'] = datetime.strptime(kwargs['booked_at'], '%Y-%m-%dT%H:%M')
        super().__init__(**kwargs)

    def __repr__(self):
        return f"Resource('{self.name}')"

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))
    resource = db.relationship('Resource', backref=db.backref('bookings', lazy=True))
    booked_at = db.Column(db.DateTime, nullable=False)
    released_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"Booking('{self.id}')"
 # type: ignore