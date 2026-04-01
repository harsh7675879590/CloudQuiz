from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Quiz, Question, Option, Attempt, Answer

student_bp = Blueprint("student", __name__)

@student_bp.route("/quizzes", methods=["GET"])
@jwt_required()
def list_available_quizzes():
    # Only active quizzes
    quizzes = Quiz.query.filter_by(is_active=True).order_by(Quiz.id.desc()).all()
    return jsonify([q.to_dict() for q in quizzes]), 200

@student_bp.route("/quizzes/<int:quiz_id>", methods=["GET"])
@jwt_required()
def get_quiz_details(quiz_id):
    quiz = Quiz.query.filter_by(id=quiz_id, is_active=True).first_or_404()
    # Strip out correct answers before sending to student!
    return jsonify(quiz.to_dict(include_questions=True)), 200

@student_bp.route("/quizzes/<int:quiz_id>/start", methods=["POST"])
@jwt_required()
def start_quiz(quiz_id):
    identity = get_jwt_identity()
    user_id = int(identity)
    
    quiz = Quiz.query.filter_by(id=quiz_id, is_active=True).first_or_404()
    
    # Check if existing unfinished attempt
    existing = Attempt.query.filter_by(user_id=user_id, quiz_id=quiz.id, finished_at=None).first()
    if existing:
        return jsonify(existing.to_dict()), 200
        
    attempt = Attempt(user_id=user_id, quiz_id=quiz.id)
    db.session.add(attempt)
    db.session.commit()
    
    return jsonify(attempt.to_dict()), 201

@student_bp.route("/attempts/<int:attempt_id>/submit", methods=["POST"])
@jwt_required()
def submit_quiz(attempt_id):
    identity = get_jwt_identity()
    user_id = int(identity)
    
    attempt = Attempt.query.filter_by(id=attempt_id, user_id=user_id).first_or_404()
    if attempt.finished_at:
        return jsonify({"error": "Quiz already submitted"}), 400
        
    quiz = attempt.quiz
    data = request.get_json()
    answers_data = data.get("answers", []) # [{"question_id": 1, "option_id": 2}]
    
    total_score = 0
    max_score = sum(q.points for q in quiz.questions)
    
    for ans in answers_data:
        q_id = ans.get("question_id")
        opt_id = ans.get("option_id")
        
        question = Question.query.get(q_id)
        if not question or question.quiz_id != quiz.id:
            continue
            
        is_correct = False
        if opt_id:
            option_obj = Option.query.get(opt_id)
            if option_obj and option_obj.question_id == q_id and option_obj.is_correct:
                is_correct = True
                total_score += question.points
                
        answer_record = Answer(
            attempt_id=attempt.id,
            question_id=q_id,
            option_id=opt_id,
            is_correct=is_correct
        )
        db.session.add(answer_record)
        
    percentage = (total_score / max_score * 100) if max_score > 0 else 0
    passed = percentage >= quiz.pass_score
    
    attempt.score = total_score
    attempt.max_score = max_score
    attempt.percentage = percentage
    attempt.passed = passed
    attempt.finished_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify(attempt.to_dict()), 200

@student_bp.route("/attempts", methods=["GET"])
@jwt_required()
def get_my_attempts():
    identity = get_jwt_identity()
    user_id = int(identity)
    attempts = Attempt.query.filter_by(user_id=user_id).order_by(Attempt.started_at.desc()).all()
    
    results = []
    for a in attempts:
        d = a.to_dict()
        d["quiz_title"] = a.quiz.title
        results.append(d)
        
    return jsonify(results), 200
