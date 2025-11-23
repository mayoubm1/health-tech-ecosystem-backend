"""
Telemedicine Routes
"""

from flask import Blueprint, request, jsonify
from app import db
from app.models import Teleconsultation, Message, Appointment
from app.utils.auth import require_auth

bp = Blueprint('telemed', __name__, url_prefix='/api/telemed')

@bp.route('/consultations', methods=['GET'])
@require_auth
def get_consultations(current_user):
    """Get consultations"""
    try:
        consultations = Teleconsultation.query.all()
        return jsonify({
            'consultations': [c.to_dict() for c in consultations]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/consultations/<consultation_id>/start', methods=['POST'])
@require_auth
def start_consultation(current_user, consultation_id):
    """Start a consultation"""
    try:
        consultation = Teleconsultation.query.get(consultation_id)
        if not consultation:
            return jsonify({'error': 'Consultation not found'}), 404
        
        consultation.status = 'in_progress'
        db.session.commit()
        
        return jsonify({
            'message': 'Consultation started',
            'consultation': consultation.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/consultations/<consultation_id>/end', methods=['POST'])
@require_auth
def end_consultation(current_user, consultation_id):
    """End a consultation"""
    try:
        consultation = Teleconsultation.query.get(consultation_id)
        if not consultation:
            return jsonify({'error': 'Consultation not found'}), 404
        
        consultation.status = 'completed'
        db.session.commit()
        
        return jsonify({
            'message': 'Consultation ended',
            'consultation': consultation.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/messages', methods=['GET'])
@require_auth
def get_messages(current_user):
    """Get messages"""
    try:
        consultation_id = request.args.get('consultation_id')
        
        if consultation_id:
            messages = Message.query.filter_by(consultation_id=consultation_id).all()
        else:
            messages = Message.query.all()
        
        return jsonify({
            'messages': [m.to_dict() for m in messages]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/messages', methods=['POST'])
@require_auth
def send_message(current_user):
    """Send a message"""
    try:
        data = request.get_json()
        
        message = Message(
            sender_id=current_user['user_id'],
            receiver_id=data.get('receiver_id'),
            consultation_id=data.get('consultation_id'),
            message_text=data.get('message_text'),
            message_type=data.get('message_type', 'text'),
            attachment_url=data.get('attachment_url')
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'message': 'Message sent',
            'data': message.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
