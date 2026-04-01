from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import db, Quiz, Question, Option, Attempt

quiz_bp = Blueprint("quizzes", __name__)

def admin_required():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return False
    return True

# ── Quizzes ────────────────────────────────────────────────────────────────────

@quiz_bp.route("/", methods=["GET"])
@jwt_required()
def get_quizzes():
    if not admin_required():
        return jsonify({"error": "Admin access required"}), 403
    
    quizzes = Quiz.query.order_by(Quiz.id.desc()).all()
    return jsonify([q.to_dict() for q in quizzes]), 200

@quiz_bp.route("/<int:quiz_id>", methods=["GET"])
@jwt_required()
def get_quiz(quiz_id):
    if not admin_required():
        return jsonify({"error": "Admin access required"}), 403
        
    quiz = Quiz.query.get_or_404(quiz_id)
    return jsonify(quiz.to_dict(include_questions=True)), 200

@quiz_bp.route("/", methods=["POST"])
@jwt_required()
def create_quiz():
    if not admin_required():
        return jsonify({"error": "Admin access required"}), 403

    identity = get_jwt_identity()
    data = request.get_json()
    
    new_quiz = Quiz(
        title=data.get("title"),
        description=data.get("description", ""),
        time_limit=data.get("time_limit", 600),
        pass_score=data.get("pass_score", 60),
        is_active=data.get("is_active", True),
        created_by=int(identity)
    )
    
    db.session.add(new_quiz)
    db.session.commit()
    
    return jsonify(new_quiz.to_dict()), 201

@quiz_bp.route("/<int:quiz_id>", methods=["PUT"])
@jwt_required()
def update_quiz(quiz_id):
    if not admin_required():
        return jsonify({"error": "Admin access required"}), 403
        
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json()
    
    quiz.title = data.get("title", quiz.title)
    quiz.description = data.get("description", quiz.description)
    quiz.time_limit = data.get("time_limit", quiz.time_limit)
    quiz.pass_score = data.get("pass_score", quiz.pass_score)
    quiz.is_active = data.get("is_active", quiz.is_active)
    
    db.session.commit()
    return jsonify(quiz.to_dict()), 200

@quiz_bp.route("/<int:quiz_id>", methods=["DELETE"])
@jwt_required()
def delete_quiz(quiz_id):
    if not admin_required():
        return jsonify({"error": "Admin access required"}), 403
        
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return jsonify({"message": "Quiz deleted"}), 200

# ── Questions & Options ────────────────────────────────────────────────────────

@quiz_bp.route("/<int:quiz_id>/questions", methods=["POST"])
@jwt_required()
def add_question(quiz_id):
    if not admin_required():
        return jsonify({"error": "Admin access required"}), 403
        
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json()
    
    question = Question(
        quiz_id=quiz.id,
        text=data.get("text"),
        points=data.get("points", 1),
        order_num=data.get("order_num", 0)
    )
    db.session.add(question)
    db.session.flush() # Get question ID
    
    options_data = data.get("options", [])
    for opt in options_data:
        option = Option(
            question_id=question.id,
            text=opt.get("text"),
            is_correct=opt.get("is_correct", False)
        )
        db.session.add(option)
        
    db.session.commit()
    return jsonify(question.to_dict(include_correct=True)), 201

@quiz_bp.route("/<int:quiz_id>/analytics", methods=["GET"])
@jwt_required()
def quiz_analytics(quiz_id):
    if not admin_required():
        return jsonify({"error": "Admin access required"}), 403
        
    quiz = Quiz.query.get_or_404(quiz_id)
    attempts = Attempt.query.filter_by(quiz_id=quiz.id).all()
    
    total = len(attempts)
    passed = sum(1 for a in attempts if a.passed)
    avg_score = sum(a.percentage for a in attempts) / total if total > 0 else 0
    
    return jsonify({
        "total_attempts": total,
        "passed": passed,
        "failed": total - passed,
        "average_score": round(avg_score, 1)
    }), 200
