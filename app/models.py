from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default="researcher", nullable=False)  # 'admin' or 'researcher'

    test_records = db.relationship("TestRecord", back_populates="added_by_user", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == "admin"

    def __repr__(self):
        return f"<User {self.username}>"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False, index=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    contact_info = db.Column(db.String(200), nullable=True)

    test_records = db.relationship("TestRecord", back_populates="patient", cascade="all, delete-orphan", lazy="dynamic")
    reports = db.relationship("Report", back_populates="patient", cascade="all, delete-orphan", lazy="dynamic")

    def __repr__(self):
        return f"<Patient {self.name}>"


class TestRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    test_type = db.Column(db.String(120), nullable=False, index=True)
    result = db.Column(db.String(5000), nullable=True)
    file_path = db.Column(db.String(255), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    added_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    added_by_user = db.relationship("User", back_populates="test_records")
    patient = db.relationship("Patient", back_populates="test_records")

    def __repr__(self):
        return f"<TestRecord {self.test_type} for patient_id={self.patient_id}>"


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    recommendation = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship("Patient", back_populates="reports")

    def __repr__(self):
        return f"<Report {self.id} for patient {self.patient_id}>"
