from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(150), unique=True, nullable=False)
    password   = db.Column(db.String(256), nullable=False)
    role       = db.Column(db.String(20), nullable=False, default='patient')  # patient | doctor | admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    readings         = db.relationship('HealthReading', foreign_keys='HealthReading.patient_id', backref='patient', lazy=True)
    assigned_patients = db.relationship('PatientDoctor', foreign_keys='PatientDoctor.doctor_id', backref='doctor', lazy=True)
    assigned_doctor  = db.relationship('PatientDoctor', foreign_keys='PatientDoctor.patient_id', backref='patient_rel', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.email}>'


class HealthReading(db.Model):
    __tablename__ = 'health_readings'
    id             = db.Column(db.Integer, primary_key=True)
    patient_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    blood_pressure_sys = db.Column(db.Integer)   # systolic
    blood_pressure_dia = db.Column(db.Integer)   # diastolic
    heart_rate     = db.Column(db.Integer)
    temperature    = db.Column(db.Float)
    blood_sugar    = db.Column(db.Float)
    notes          = db.Column(db.Text)
    is_flagged     = db.Column(db.Boolean, default=False)
    recorded_at    = db.Column(db.DateTime, default=datetime.utcnow)

    def check_alerts(self):
        flags = []
        if self.blood_pressure_sys and self.blood_pressure_sys > 140:
            flags.append('High systolic blood pressure')
        if self.blood_pressure_dia and self.blood_pressure_dia > 90:
            flags.append('High diastolic blood pressure')
        if self.heart_rate and (self.heart_rate < 50 or self.heart_rate > 110):
            flags.append('Abnormal heart rate')
        if self.temperature and (self.temperature < 35.0 or self.temperature > 38.5):
            flags.append('Abnormal temperature')
        if self.blood_sugar and (self.blood_sugar < 70 or self.blood_sugar > 180):
            flags.append('Abnormal blood sugar')
        return flags


class PatientDoctor(db.Model):
    __tablename__ = 'patient_doctor'
    id         = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id  = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class DoctorNote(db.Model):
    __tablename__ = 'doctor_notes'
    id         = db.Column(db.Integer, primary_key=True)
    reading_id = db.Column(db.Integer, db.ForeignKey('health_readings.id'), nullable=False)
    doctor_id  = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    note       = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reading = db.relationship('HealthReading', backref='doctor_notes')
    doctor  = db.relationship('User', backref='notes_written')
