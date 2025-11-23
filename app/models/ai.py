"""
AI Models - AIModel, AIAgent, AIInteraction
"""

from datetime import datetime
from app import db
import uuid

class AIModel(db.Model):
    """AI Model for managing integrated AI models"""
    __tablename__ = 'ai_models'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    model_type = db.Column(db.String(100))  # language_model, image_model, classification, etc.
    api_endpoint = db.Column(db.String(500))
    api_key_id = db.Column(db.String(36))
    version = db.Column(db.String(50))
    status = db.Column(db.String(50), default='active')  # active, inactive, maintenance
    capabilities = db.Column(db.JSON, default=list)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ai_agents = db.relationship('AIAgent', backref='model', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'model_type': self.model_type,
            'api_endpoint': self.api_endpoint,
            'version': self.version,
            'status': self.status,
            'capabilities': self.capabilities,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class AIAgent(db.Model):
    """AI Agent for managing AI agent instances"""
    __tablename__ = 'ai_agents'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), unique=True, nullable=False, index=True)
    model_id = db.Column(db.String(36), db.ForeignKey('ai_models.id'), nullable=False)
    description = db.Column(db.Text)
    configuration = db.Column(db.JSON)
    owner_user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), default='active')  # active, inactive, testing
    purpose = db.Column(db.String(255))  # diagnosis_support, treatment_recommendation, etc.
    accuracy_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = db.relationship('User', backref='owned_ai_agents')
    ai_interactions = db.relationship('AIInteraction', backref='agent', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'model_id': self.model_id,
            'description': self.description,
            'configuration': self.configuration,
            'owner_user_id': self.owner_user_id,
            'status': self.status,
            'purpose': self.purpose,
            'accuracy_score': self.accuracy_score,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class AIInteraction(db.Model):
    """AI Interaction for logging AI agent interactions"""
    __tablename__ = 'ai_interactions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = db.Column(db.String(36), db.ForeignKey('ai_agents.id'), nullable=False, index=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    input_data = db.Column(db.JSON)
    output_data = db.Column(db.JSON)
    interaction_type = db.Column(db.String(100))  # query, analysis, recommendation, etc.
    confidence_score = db.Column(db.Float)
    processing_time_ms = db.Column(db.Integer)
    interaction_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    feedback_score = db.Column(db.Integer)  # 1-5 rating from user
    
    # Relationships
    user = db.relationship('User', backref='ai_interactions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'user_id': self.user_id,
            'input_data': self.input_data,
            'output_data': self.output_data,
            'interaction_type': self.interaction_type,
            'confidence_score': self.confidence_score,
            'processing_time_ms': self.processing_time_ms,
            'interaction_time': self.interaction_time.isoformat(),
            'feedback_score': self.feedback_score
        }
