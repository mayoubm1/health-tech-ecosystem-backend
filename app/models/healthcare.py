"""
Healthcare Models - Patient, Provider, Appointment, Medical Records
"""

from datetime import datetime
from app import db
import uuid
import json

class Patient(db.Model):
    """Patient model for patient information and medical history"""
    __tablename__ = 'patients'
    
    id = db.Column(db.String(36), db.ForeignKey('users.id'), primary_key=True)
    ehr_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    medical_history = db.Column(db.JSON)
    allergies = db.Column(db.JSON, default=list)
    current_medications = db.Column(db.JSON, default=list)
    primary_care_provider_id = db.Column(db.String(36), db.ForeignKey('healthcare_providers.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='patient', lazy=True, cascade='all, delete-orphan')
    medical_records = db.relationship('MedicalRecord', backref='patient', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'ehr_id': self.ehr_id,
            'medical_history': self.medical_history,
            'allergies': self.allergies,
            'current_medications': self.current_medications,
            'primary_care_provider_id': self.primary_care_provider_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class HealthcareProvider(db.Model):
    """Healthcare Provider model for doctor/provider information"""
    __tablename__ = 'healthcare_providers'
    
    id = db.Column(db.String(36), db.ForeignKey('users.id'), primary_key=True)
    license_number = db.Column(db.String(100), unique=True, nullable=False, index=True)
    specialization = db.Column(db.String(100))
    clinic_address = db.Column(db.String(255))
    clinic_phone = db.Column(db.String(20))
    years_of_experience = db.Column(db.Integer)
    bio = db.Column(db.Text)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patients = db.relationship('Patient', backref='primary_care_provider', lazy=True)
    appointments = db.relationship('Appointment', backref='provider', lazy=True, cascade='all, delete-orphan')
    medical_records = db.relationship('MedicalRecord', backref='provider', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'license_number': self.license_number,
            'specialization': self.specialization,
            'clinic_address': self.clinic_address,
            'clinic_phone': self.clinic_phone,
            'years_of_experience': self.years_of_experience,
            'bio': self.bio,
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Appointment(db.Model):
    """Appointment model for scheduling appointments"""
    __tablename__ = 'appointments'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String(36), db.ForeignKey('patients.id'), nullable=False)
    provider_id = db.Column(db.String(36), db.ForeignKey('healthcare_providers.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, index=True)
    end_time = db.Column(db.DateTime, nullable=False)
    appointment_type = db.Column(db.String(50), nullable=False)  # telemedicine, in_person, follow_up
    status = db.Column(db.String(50), default='scheduled')  # scheduled, completed, cancelled, no_show
    reason = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    teleconsultation = db.relationship('Teleconsultation', backref='appointment', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'provider_id': self.provider_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'appointment_type': self.appointment_type,
            'status': self.status,
            'reason': self.reason,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class MedicalRecord(db.Model):
    """Medical Record model for storing patient medical records"""
    __tablename__ = 'medical_records'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String(36), db.ForeignKey('patients.id'), nullable=False)
    provider_id = db.Column(db.String(36), db.ForeignKey('healthcare_providers.id'), nullable=False)
    record_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    record_type = db.Column(db.String(50))  # diagnosis, treatment, prescription, lab_result, imaging
    diagnosis = db.Column(db.Text)
    treatment = db.Column(db.Text)
    prescription = db.Column(db.JSON)
    lab_results = db.Column(db.JSON)
    attachments = db.Column(db.JSON, default=list)  # URLs to files in storage
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'provider_id': self.provider_id,
            'record_date': self.record_date.isoformat(),
            'record_type': self.record_type,
            'diagnosis': self.diagnosis,
            'treatment': self.treatment,
            'prescription': self.prescription,
            'lab_results': self.lab_results,
            'attachments': self.attachments,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
