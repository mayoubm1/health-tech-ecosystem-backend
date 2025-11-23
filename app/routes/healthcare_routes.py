"""
Healthcare Routes - Patients, Providers, Appointments, Medical Records
"""

from flask import Blueprint, request, jsonify
from app import db
from app.models import Patient, HealthcareProvider, Appointment, MedicalRecord, User
from app.utils.auth import verify_jwt_token, require_auth
from datetime import datetime

bp = Blueprint('healthcare', __name__, url_prefix='/api/healthcare')

# Patient Routes
@bp.route('/patients', methods=['GET'])
@require_auth
def get_patients(current_user):
    """Get all patients or filter by provider"""
    try:
        if current_user['role'] == 'healthcare_provider':
            patients = Patient.query.filter_by(primary_care_provider_id=current_user['user_id']).all()
        elif current_user['role'] == 'admin':
            patients = Patient.query.all()
        else:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify({
            'patients': [p.to_dict() for p in patients]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/patients/<patient_id>', methods=['GET'])
@require_auth
def get_patient(current_user, patient_id):
    """Get patient details"""
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Check authorization
        if current_user['role'] == 'patient' and current_user['user_id'] != patient_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify({
            'patient': patient.to_dict(),
            'user': patient.user.to_dict() if patient.user else None
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/patients', methods=['POST'])
@require_auth
def create_patient(current_user):
    """Create a new patient"""
    try:
        if current_user['role'] not in ['admin', 'healthcare_provider']:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        # Check if user exists
        user = User.query.get(data.get('user_id'))
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Create patient record
        patient = Patient(
            id=data['user_id'],
            ehr_id=data.get('ehr_id'),
            medical_history=data.get('medical_history'),
            allergies=data.get('allergies', []),
            current_medications=data.get('current_medications', []),
            primary_care_provider_id=data.get('primary_care_provider_id')
        )
        
        db.session.add(patient)
        db.session.commit()
        
        return jsonify({
            'message': 'Patient created successfully',
            'patient': patient.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Appointment Routes
@bp.route('/appointments', methods=['GET'])
@require_auth
def get_appointments(current_user):
    """Get appointments"""
    try:
        if current_user['role'] == 'patient':
            appointments = Appointment.query.filter_by(patient_id=current_user['user_id']).all()
        elif current_user['role'] == 'healthcare_provider':
            appointments = Appointment.query.filter_by(provider_id=current_user['user_id']).all()
        elif current_user['role'] == 'admin':
            appointments = Appointment.query.all()
        else:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify({
            'appointments': [a.to_dict() for a in appointments]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/appointments', methods=['POST'])
@require_auth
def create_appointment(current_user):
    """Create a new appointment"""
    try:
        data = request.get_json()
        
        appointment = Appointment(
            patient_id=data.get('patient_id'),
            provider_id=data.get('provider_id'),
            start_time=datetime.fromisoformat(data.get('start_time')),
            end_time=datetime.fromisoformat(data.get('end_time')),
            appointment_type=data.get('appointment_type', 'in_person'),
            reason=data.get('reason'),
            notes=data.get('notes')
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        return jsonify({
            'message': 'Appointment created successfully',
            'appointment': appointment.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/appointments/<appointment_id>', methods=['PUT'])
@require_auth
def update_appointment(current_user, appointment_id):
    """Update appointment status"""
    try:
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        data = request.get_json()
        
        if 'status' in data:
            appointment.status = data['status']
        if 'notes' in data:
            appointment.notes = data['notes']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Appointment updated successfully',
            'appointment': appointment.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Medical Records Routes
@bp.route('/medical-records', methods=['GET'])
@require_auth
def get_medical_records(current_user):
    """Get medical records"""
    try:
        patient_id = request.args.get('patient_id')
        
        if current_user['role'] == 'patient':
            records = MedicalRecord.query.filter_by(patient_id=current_user['user_id']).all()
        elif current_user['role'] == 'healthcare_provider':
            records = MedicalRecord.query.filter_by(provider_id=current_user['user_id']).all()
        elif current_user['role'] == 'admin' and patient_id:
            records = MedicalRecord.query.filter_by(patient_id=patient_id).all()
        else:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify({
            'medical_records': [r.to_dict() for r in records]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/medical-records', methods=['POST'])
@require_auth
def create_medical_record(current_user):
    """Create a new medical record"""
    try:
        if current_user['role'] != 'healthcare_provider':
            return jsonify({'error': 'Only healthcare providers can create medical records'}), 403
        
        data = request.get_json()
        
        record = MedicalRecord(
            patient_id=data.get('patient_id'),
            provider_id=current_user['user_id'],
            record_type=data.get('record_type'),
            diagnosis=data.get('diagnosis'),
            treatment=data.get('treatment'),
            prescription=data.get('prescription'),
            lab_results=data.get('lab_results'),
            attachments=data.get('attachments', [])
        )
        
        db.session.add(record)
        db.session.commit()
        
        return jsonify({
            'message': 'Medical record created successfully',
            'medical_record': record.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
