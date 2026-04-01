import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from config import Config
from models import db
from auth import auth_bp
from quiz_routes import quiz_bp
from student_routes import student_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Extensions
    db.init_app(app)
    JWTManager(app)
    CORS(app, resources={r"/*": {"origins": app.config["CORS_ORIGINS"]}})

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(quiz_bp, url_prefix='/api/quizzes')
    app.register_blueprint(student_bp, url_prefix='/api/student')

    # Health check endpoint for AWS Target Group or general monitoring
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "ok",
            "message": "Online Quiz API is running."
        }), 200

    # Ensure tables exist (In production, use Flask-Migrate instead!)
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])
