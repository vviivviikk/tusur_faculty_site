from .base import db

class UserRights(db.Model):
    __tablename__ = 'User_rights'

    User_id = db.Column(db.Integer, db.ForeignKey('User_data.User_id'), primary_key=True)
    User_type = db.Column(db.String(10), nullable=False)

    user = db.relationship("UserData", back_populates="rights")
