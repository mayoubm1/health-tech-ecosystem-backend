"""
Models Package - Import all models
"""

from app.models.user import User, Profile
from app.models.healthcare import Patient, HealthcareProvider, Appointment, MedicalRecord
from app.models.telemed import Teleconsultation, Message
from app.models.research import ResearchProject, Dataset, Collaboration, ResearchOutput
from app.models.ai import AIModel, AIAgent, AIInteraction

__all__ = [
    'User',
    'Profile',
    'Patient',
    'HealthcareProvider',
    'Appointment',
    'MedicalRecord',
    'Teleconsultation',
    'Message',
    'ResearchProject',
    'Dataset',
    'Collaboration',
    'ResearchOutput',
    'AIModel',
    'AIAgent',
    'AIInteraction'
]
