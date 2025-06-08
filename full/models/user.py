from .base import db

class UserData(db.Model):
    __tablename__ = 'User_data'

    User_id = db.Column(db.Integer, primary_key=True)
    Telegram_user_id = db.Column(db.Integer, nullable=True)
    FIO = db.Column(db.String(255), nullable=False)
    Date_brith = db.Column(db.Date, nullable=False)
    Gender = db.Column(db.String(10), nullable=False)
    Year_grad_fr_school = db.Column(db.Integer, nullable=False)

    rights = db.relationship(
        "UserRights", back_populates="user",
        uselist=False, cascade="all, delete-orphan"
    )
    contacts = db.relationship(
        "UsersContacts", back_populates="user",
        uselist=False, cascade="all, delete-orphan"
    )
    faculties = db.relationship(
        "UserFaculty", back_populates="user",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "User_id": self.User_id,
            "Telegram_user_id": self.Telegram_user_id,
            "FIO": self.FIO,
            "Date_brith": self.Date_brith.isoformat(),
            "Gender": self.Gender,
            "Year_grad_fr_school": self.Year_grad_fr_school,
            "rights": self.rights.User_type if self.rights else None,
            "contacts": {"email": self.contacts.Email, "phone": self.contacts.Phone}
            if self.contacts
            else None,
            "faculties": [f.faculty.Faculty_name for f in self.faculties]
            if self.faculties
            else [],
        }
