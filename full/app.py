from flask import Flask, render_template, redirect, jsonify, request
from models import db
from models import UserData, UserRights, UsersContacts, Faculty, UserFaculty
from datetime import date


app= Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/snack/edu/full/full/testDB.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/faculty")
def faculty():
    return render_template('faculty.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/auth")
def auth():
    return render_template('auth.html')


@app.route("/users", methods=["POST"])
def create():
    data = request.form or request.json

    user = UserData(
        FIO=data["FIO"],
        Date_brith=date.fromisoformat(data["Date_brith"]),
        Gender=data["Gender"],
        Year_grad_fr_school=int(data["Year_grad_fr_school"]),
        Telegram_user_id=data.get("Telegram_user_id"),
    )

    db.session.add(user)
    db.session.flush()

    rights = UserRights(User_id=user.User_id, User_type=data.get("User_type", "User"))
    contacts = UsersContacts(
        User_id=user.User_id, Email=data.get("Email"), Phone=data.get("Phone")
    )

    db.session.add_all([rights, contacts])
    db.session.commit()

    return jsonify({"status": "created", "user_id": user.User_id})

@app.route("/users/<int:user_id>", methods=["GET"])
def show(user_id):
    user = UserData.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())

@app.route("/users", methods=["GET"])
def user_index():
    users = UserData.query.all()
    result = [
        {
            "id": user.User_id,
            "fio": user.FIO,
            "year": user.Year_grad_fr_school,
            "type": user.rights.User_type if user.rights else None,
        }
        for user in users
    ]
    return jsonify(result)

@app.route("/users/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = UserData.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json

    user.FIO = data.get("FIO", user.FIO)
    user.Telegram_user_id = data.get("Telegram_user_id", user.Telegram_user_id)
    user.Gender = data.get("Gender", user.Gender)
    user.Year_grad_fr_school = data.get("Year_grad_fr_school", user.Year_grad_fr_school)

    if "Date_brith" in data:
        from datetime import date
        user.Date_brith = date.fromisoformat(data["Date_brith"])

    db.session.commit()
    return jsonify(user.to_dict())

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = UserData.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.rights:
        db.session.delete(user.rights)
    if user.contacts:
        db.session.delete(user.contacts)
    for uf in user.faculties:
        db.session.delete(uf)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"status": "User deleted"})

if __name__ == '__main__':
    app.run(debug=True)
