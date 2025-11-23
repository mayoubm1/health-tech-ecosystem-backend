"""
Telemedicine Models - Teleconsultation, Messages
"""

from datetime import datetime
from app import db
import uuid

class Teleconsultation(db.Model):
    """Teleconsultation model for virtual consultations"""
    __tablename__ = 'teleconsultations'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    appointment_id = db.Column(db.String(36), db.ForeignKey('appointments.id'), unique=True, nullable=False)
    consultation_url = db.Column(db.String(500))
    meeting_code = db.Column(db.String(100), unique=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='pending')  # pending, in_progress, completed, cancelled
    duration_minutes = db.Column(db.Integer)
    transcript = db.Column(db.Text)
    recording_url = db.Column(db.String(500))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = db.relationship('Message', backref='teleconsultation', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'appointment_id': self.appointment_id,
            'consultation_url': self.consultation_url,
            'meeting_code': self.meeting_code,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'status': self.status,
            'duration_minutes': self.duration_minutes,
            'transcript': self.transcript,
            'recording_url': self.recording_url,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Message(db.Model):
    """Message model for real-time chat during consultations"""
    __tablename__ = 'messages'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sender_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    receiver_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    consultation_id = db.Column(db.String(36), db.ForeignKey('teleconsultations.id'), nullable=True, index=True)
    message_text = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(50), default='text')  # text, image, file, system
    attachment_url = db.Column(db.String(500))
    sent_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    read_at = db.Column(db.DateTime)
    is_edited = db.Column(db.Boolean, default=False)
    edited_at = db.Column(db.DateTime)
    
    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')
    
    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'consultation_id': self.consultation_id,
            'message_text': self.message_text,
            'message_type': self.message_type,
            'attachment_url': self.attachment_url,
            'sent_at': self.sent_at.isoformat(),
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'is_edited': self.is_edited,
            'edited_at': self.edited_at.isoformat() if self.edited_at else None
        }
