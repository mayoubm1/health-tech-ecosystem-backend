"""
Research Models - ResearchProject, Dataset, Collaboration, ResearchOutput
"""

from datetime import datetime
from app import db
import uuid

class ResearchProject(db.Model):
    """Research Project model for managing research initiatives"""
    __tablename__ = 'research_projects'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='planning')  # planning, in_progress, completed, archived
    lead_researcher_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    budget = db.Column(db.Float)
    funding_source = db.Column(db.String(255))
    keywords = db.Column(db.JSON, default=list)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    datasets = db.relationship('Dataset', backref='project', lazy=True, cascade='all, delete-orphan')
    collaborations = db.relationship('Collaboration', backref='project', lazy=True, cascade='all, delete-orphan')
    research_outputs = db.relationship('ResearchOutput', backref='project', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'lead_researcher_id': self.lead_researcher_id,
            'budget': self.budget,
            'funding_source': self.funding_source,
            'keywords': self.keywords,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Dataset(db.Model):
    """Dataset model for storing research data"""
    __tablename__ = 'datasets'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey('research_projects.id'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    storage_url = db.Column(db.String(500))
    file_size_mb = db.Column(db.Float)
    data_format = db.Column(db.String(50))  # csv, json, xlsx, parquet, etc.
    data_schema = db.Column(db.JSON)
    access_level = db.Column(db.String(50), default='private')  # public, restricted, private
    uploaded_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    last_accessed_at = db.Column(db.DateTime)
    download_count = db.Column(db.Integer, default=0)
    
    # Relationships
    uploader = db.relationship('User', backref='uploaded_datasets')
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'name': self.name,
            'description': self.description,
            'storage_url': self.storage_url,
            'file_size_mb': self.file_size_mb,
            'data_format': self.data_format,
            'data_schema': self.data_schema,
            'access_level': self.access_level,
            'uploaded_by': self.uploaded_by,
            'uploaded_at': self.uploaded_at.isoformat(),
            'last_accessed_at': self.last_accessed_at.isoformat() if self.last_accessed_at else None,
            'download_count': self.download_count
        }

class Collaboration(db.Model):
    """Collaboration model for managing research team members"""
    __tablename__ = 'collaborations'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey('research_projects.id'), nullable=False, index=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    role = db.Column(db.String(50), nullable=False)  # principal_investigator, co_investigator, data_analyst, contributor
    permissions = db.Column(db.JSON, default=list)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    user = db.relationship('User', backref='collaborations')
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'role': self.role,
            'permissions': self.permissions,
            'joined_at': self.joined_at.isoformat(),
            'is_active': self.is_active
        }

class ResearchOutput(db.Model):
    """Research Output model for publications and deliverables"""
    __tablename__ = 'research_outputs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey('research_projects.id'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    output_type = db.Column(db.String(50), nullable=False)  # publication, report, presentation, code, dataset
    publication_date = db.Column(db.Date)
    url = db.Column(db.String(500))
    doi = db.Column(db.String(100))
    authors = db.Column(db.JSON, default=list)
    citations_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'title': self.title,
            'description': self.description,
            'output_type': self.output_type,
            'publication_date': self.publication_date.isoformat() if self.publication_date else None,
            'url': self.url,
            'doi': self.doi,
            'authors': self.authors,
            'citations_count': self.citations_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
