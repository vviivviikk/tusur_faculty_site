from .base import db

class UsersContacts(db.Model):
    __tablename__ = 'Users_contacts'

    User_id = db.Column(db.Integer, db.ForeignKey('User_data.User_id'), primary_key=True)
    Email = db.Column(db.String(255), nullable=True)
    Phone = db.Column(db.String(20), nullable=True)

    user = db.relationship("UserData", back_populates="contacts")
