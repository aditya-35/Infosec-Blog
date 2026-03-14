from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "secret-key-for-project"

# Configuration for SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Configuration for Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# --- Models ---
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    # Relationship to records
    records = db.relationship('Record', backref='owner', lazy=True)

class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Application Context Initialization ---
with app.app_context():
    # Attempt to create tables, but SQLite won't easily migrate if the schema already exists
    # from the older version. For a clean slate, it's best to overwrite/delete the db,
    # or handle migration. We'll simply call create_all(), which will create tables 
    # if they completely don't exist.
    db.create_all()

# --- Routes ---
@app.route("/", methods=["GET"])
@login_required
def index():
    # SQLAlchemy query for current user's records
    records = Record.query.filter_by(user_id=current_user.id).all()
    return render_template("index.html", records=records)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Basic Check
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/add", methods=["POST"])
@login_required
def add():
    title = request.form["title"]
    description = request.form["description"]
    
    new_record = Record(title=title, description=description, user_id=current_user.id)
    db.session.add(new_record)
    db.session.commit()
    
    return redirect(url_for("index"))

@app.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id):
    # Fetch the record, ensuring it belongs to the current user
    record = Record.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    if request.method == "POST":
        record.title = request.form["title"]
        record.description = request.form["description"]
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("update.html", record=record)

@app.route("/delete/<int:id>")
@login_required
def delete(id):
    # Fetch the record, ensuring it belongs to the current user
    record = Record.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    db.session.delete(record)
    db.session.commit()
    
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
