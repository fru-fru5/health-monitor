from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, PatientDoctor

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    users    = User.query.order_by(User.created_at.desc()).all()
    patients = [u for u in users if u.role == 'patient']
    doctors  = [u for u in users if u.role == 'doctor']
    return render_template('admin/dashboard.html', users=users, patients=patients, doctors=doctors)

@admin_bp.route('/assign', methods=['POST'])
@login_required
def assign():
    patient_id = request.form.get('patient_id', type=int)
    doctor_id  = request.form.get('doctor_id', type=int)
    existing   = PatientDoctor.query.filter_by(patient_id=patient_id, doctor_id=doctor_id).first()
    if not existing:
        assignment = PatientDoctor(patient_id=patient_id, doctor_id=doctor_id)
        db.session.add(assignment)
        db.session.commit()
        flash('Patient assigned to doctor successfully.', 'success')
    else:
        flash('This assignment already exists.', 'info')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.name} has been removed.', 'success')
    return redirect(url_for('admin.dashboard'))
