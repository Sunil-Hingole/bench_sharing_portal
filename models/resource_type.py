from flask_sqlalchemy import SQLAlchemy
from models import db


class ResourceType(db.Model):
    __tablename__ = 'resource_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return ResourceType.query.all()

    @staticmethod
    def get_by_id(id):
        return ResourceType.query.get(id)

    @staticmethod
    def update(id, name, description):
        resource_type = ResourceType.query.get(id)
        resource_type.name = name
        resource_type.description = description
        db.session.commit()

    @staticmethod
    def delete(id):
        resource_type = ResourceType.query.get(id)
        db.session.delete(resource_type)
        db.session.commit()
