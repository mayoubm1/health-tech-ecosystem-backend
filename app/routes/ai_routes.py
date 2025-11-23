"""
AI Routes - OmniCognitor
"""

from flask import Blueprint, request, jsonify
from app import db
from app.models import AIModel, AIAgent, AIInteraction
from app.utils.auth import require_auth

bp = Blueprint('ai', __name__, url_prefix='/api/ai')

@bp.route('/models', methods=['GET'])
@require_auth
def get_models(current_user):
    """Get available AI models"""
    try:
        models = AIModel.query.filter_by(status='active').all()
        return jsonify({
            'models': [m.to_dict() for m in models]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/models/<model_id>', methods=['GET'])
@require_auth
def get_model(current_user, model_id):
    """Get model details"""
    try:
        model = AIModel.query.get(model_id)
        if not model:
            return jsonify({'error': 'Model not found'}), 404
        
        return jsonify({
            'model': model.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/agents', methods=['GET'])
@require_auth
def get_agents(current_user):
    """Get AI agents"""
    try:
        agents = AIAgent.query.filter_by(status='active').all()
        return jsonify({
            'agents': [a.to_dict() for a in agents]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/agents/<agent_id>', methods=['GET'])
@require_auth
def get_agent(current_user, agent_id):
    """Get agent details"""
    try:
        agent = AIAgent.query.get(agent_id)
        if not agent:
            return jsonify({'error': 'Agent not found'}), 404
        
        return jsonify({
            'agent': agent.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/agents', methods=['POST'])
@require_auth
def create_agent(current_user):
    """Create a new AI agent"""
    try:
        if current_user['role'] != 'ai_admin':
            return jsonify({'error': 'Only AI admins can create agents'}), 403
        
        data = request.get_json()
        
        agent = AIAgent(
            name=data.get('name'),
            model_id=data.get('model_id'),
            description=data.get('description'),
            configuration=data.get('configuration'),
            owner_user_id=current_user['user_id'],
            purpose=data.get('purpose'),
            accuracy_score=data.get('accuracy_score')
        )
        
        db.session.add(agent)
        db.session.commit()
        
        return jsonify({
            'message': 'Agent created successfully',
            'agent': agent.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/agents/<agent_id>/interact', methods=['POST'])
@require_auth
def interact_with_agent(current_user, agent_id):
    """Interact with an AI agent"""
    try:
        agent = AIAgent.query.get(agent_id)
        if not agent:
            return jsonify({'error': 'Agent not found'}), 404
        
        data = request.get_json()
        
        # Log interaction
        interaction = AIInteraction(
            agent_id=agent_id,
            user_id=current_user['user_id'],
            input_data=data.get('input'),
            interaction_type=data.get('interaction_type', 'query'),
            output_data={'status': 'processing'}
        )
        
        db.session.add(interaction)
        db.session.commit()
        
        return jsonify({
            'message': 'Interaction logged',
            'interaction': interaction.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/interactions', methods=['GET'])
@require_auth
def get_interactions(current_user):
    """Get user's AI interactions"""
    try:
        interactions = AIInteraction.query.filter_by(user_id=current_user['user_id']).all()
        return jsonify({
            'interactions': [i.to_dict() for i in interactions]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
