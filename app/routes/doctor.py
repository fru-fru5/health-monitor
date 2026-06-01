from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, HealthReading, PatientDoctor, DoctorNote

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/dashboard')
@login_required
def dashboard():
    assignments = PatientDoctor.query.filter_by(doctor_id=current_user.id).all()
    patient_ids = [a.patient_id for a in assignments]
    patients    = User.query.filter(User.id.in_(patient_ids)).all()
    flagged     = HealthReading.query.filter(
                    HealthReading.patient_id.in_(patient_ids),
                    HealthReading.is_flagged == True
                  ).order_by(HealthReading.recorded_at.desc()).limit(10).all()
    return render_template('doctor/dashboard.html', patients=patients, flagged=flagged)

@doctor_bp.route('/patient/<int:patient_id>')
@login_required
def patient_detail(patient_id):
    patient  = User.query.get_or_404(patient_id)
    readings = HealthReading.query.filter_by(patient_id=patient_id)\
                .order_by(HealthReading.recorded_at.desc()).all()
    return render_template('doctor/patient_detail.html', patient=patient, readings=readings)

@doctor_bp.route('/add-note/<int:reading_id>', methods=['POST'])
@login_required
def add_note(reading_id):
    note_text = request.form.get('note')
    note = DoctorNote(reading_id=reading_id, doctor_id=current_user.id, note=note_text)
    db.session.add(note)
    db.session.commit()
    flash('Note added successfully.', 'success')
    return redirect(request.referrer)
