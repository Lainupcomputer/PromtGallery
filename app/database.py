"""
This module initializes and provides an instance of SQLAlchemy, for database interactions.
DImage provides ORM
"""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class DImage(db.Model):
    __tablename__ = 'Images'
    id = db.Column(db.Integer, primary_key=True)
    positive = db.Column(db.String)
    negative = db.Column(db.String)
    img_path = db.Column(db.String)