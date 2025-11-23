"""
Research Routes
"""

from flask import Blueprint, request, jsonify
from app import db
from app.models import ResearchProject, Dataset, Collaboration, ResearchOutput
from app.utils.auth import require_auth

bp = Blueprint('research', __name__, url_prefix='/api/research')

@bp.route('/projects', methods=['GET'])
@require_auth
def get_projects(current_user):
    """Get research projects"""
    try:
        projects = ResearchProject.query.all()
        return jsonify({
            'projects': [p.to_dict() for p in projects]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/projects/<project_id>', methods=['GET'])
@require_auth
def get_project(current_user, project_id):
    """Get project details"""
    try:
        project = ResearchProject.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        return jsonify({
            'project': project.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/projects', methods=['POST'])
@require_auth
def create_project(current_user):
    """Create a new research project"""
    try:
        if current_user['role'] != 'researcher':
            return jsonify({'error': 'Only researchers can create projects'}), 403
        
        data = request.get_json()
        
        project = ResearchProject(
            name=data.get('name'),
            description=data.get('description'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            lead_researcher_id=current_user['user_id'],
            budget=data.get('budget'),
            funding_source=data.get('funding_source'),
            keywords=data.get('keywords', [])
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({
            'message': 'Project created successfully',
            'project': project.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/projects/<project_id>/datasets', methods=['GET'])
@require_auth
def get_datasets(current_user, project_id):
    """Get datasets for a project"""
    try:
        datasets = Dataset.query.filter_by(project_id=project_id).all()
        return jsonify({
            'datasets': [d.to_dict() for d in datasets]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/projects/<project_id>/datasets', methods=['POST'])
@require_auth
def upload_dataset(current_user, project_id):
    """Upload a dataset"""
    try:
        data = request.get_json()
        
        dataset = Dataset(
            project_id=project_id,
            name=data.get('name'),
            description=data.get('description'),
            storage_url=data.get('storage_url'),
            file_size_mb=data.get('file_size_mb'),
            data_format=data.get('data_format'),
            data_schema=data.get('data_schema'),
            access_level=data.get('access_level', 'private'),
            uploaded_by=current_user['user_id']
        )
        
        db.session.add(dataset)
        db.session.commit()
        
        return jsonify({
            'message': 'Dataset uploaded successfully',
            'dataset': dataset.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/projects/<project_id>/collaborations', methods=['GET'])
@require_auth
def get_collaborations(current_user, project_id):
    """Get project collaborations"""
    try:
        collaborations = Collaboration.query.filter_by(project_id=project_id).all()
        return jsonify({
            'collaborations': [c.to_dict() for c in collaborations]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/projects/<project_id>/outputs', methods=['GET'])
@require_auth
def get_outputs(current_user, project_id):
    """Get research outputs"""
    try:
        outputs = ResearchOutput.query.filter_by(project_id=project_id).all()
        return jsonify({
            'outputs': [o.to_dict() for o in outputs]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
