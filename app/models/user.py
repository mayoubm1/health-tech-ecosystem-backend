"""
User and Profile Models
"""

from datetime import datetime
from app import db
import uuid

class User(db.Model):
    """User model for authentication and authorization"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='patient')  # admin, healthcare_provider, patient, researcher, ai_admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profile = db.relationship('Profile', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Profile(db.Model):
    """User Profile model for additional user information"""
    __tablename__ = 'profiles'
    
    id = db.Column(db.String(36), db.ForeignKey('users.id'), primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    gender = db.Column(db.String(20))  # male, female, other
    profile_picture_url = db.Column(db.String(500))
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'address': self.address,
            'phone_number': self.phone_number,
            'gender': self.gender,
            'profile_picture_url': self.profile_picture_url,
            'bio': self.bio,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
