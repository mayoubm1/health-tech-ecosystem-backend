"""
Health Tech Ecosystem - Flask Backend Application
Main entry point for the backend API server
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()

def create_app(config_name='development'):
    """Application factory function"""
    
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'postgresql://user:password@localhost:5432/health_tech_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    app.config['JWT_SECRET'] = os.getenv('JWT_SECRET', 'your-jwt-secret-change-in-production')
    
    # CORS Configuration
    CORS(app, resources={
        r"/api/*": {
            "origins": os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(','),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Register blueprints
    from app.routes import auth_routes, healthcare_routes, telemed_routes, research_routes, ai_routes
    
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(healthcare_routes.bp)
    app.register_blueprint(telemed_routes.bp)
    app.register_blueprint(research_routes.bp)
    app.register_blueprint(ai_routes.bp)
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'Health Tech Ecosystem Backend',
            'version': '1.0.0'
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
