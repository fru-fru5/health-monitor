from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import HealthReading

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/dashboard')
@login_required
def dashboard():
    readings = HealthReading.query.filter_by(patient_id=current_user.id)\
                .order_by(HealthReading.recorded_at.desc()).limit(10).all()
    flagged  = [r for r in readings if r.is_flagged]
    return render_template('patient/dashboard.html', readings=readings, flagged=flagged)

@patient_bp.route('/add-reading', methods=['GET', 'POST'])
@login_required
def add_reading():
    if request.method == 'POST':
        reading = HealthReading(
            patient_id         = current_user.id,
            blood_pressure_sys = request.form.get('bp_sys', type=int),
            blood_pressure_dia = request.form.get('bp_dia', type=int),
            heart_rate         = request.form.get('heart_rate', type=int),
            temperature        = request.form.get('temperature', type=float),
            blood_sugar        = request.form.get('blood_sugar', type=float),
            notes              = request.form.get('notes')
        )
        alerts = reading.check_alerts()
        if alerts:
            reading.is_flagged = True
            for alert in alerts:
                flash(f'Alert: {alert}', 'warning')
        else:
            flash('Reading recorded successfully.', 'success')
        db.session.add(reading)
        db.session.commit()
        return redirect(url_for('patient.dashboard'))
    return render_template('patient/add_reading.html')

@patient_bp.route('/history')
@login_required
def history():
    readings = HealthReading.query.filter_by(patient_id=current_user.id)\
                .order_by(HealthReading.recorded_at.desc()).all()
    return render_template('patient/history.html', readings=readings)
