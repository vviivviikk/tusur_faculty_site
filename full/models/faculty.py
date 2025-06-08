from .base import db

class Faculty(db.Model):
    __tablename__ = 'Faculty'

    Faculty_id = db.Column(db.Integer, primary_key=True)
    Faculty_name = db.Column(db.String(255), nullable=False)

    users = db.relationship(
        "UserFaculty", back_populates="faculty", cascade="all, delete-orphan"
    )


class UserFaculty(db.Model):
    __tablename__ = 'User_faculty'

    User_id = db.Column(db.Integer, db.ForeignKey('User_data.User_id'), primary_key=True)
    Faculty_id = db.Column(db.Integer, db.ForeignKey('Faculty.Faculty_id'), primary_key=True)

    user = db.relationship("UserData", back_populates="faculties")
    faculty = db.relationship("Faculty", back_populates="users")
