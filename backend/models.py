from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# ── User ───────────────────────────────────────────────────────────────────────
class User(db.Model):
    __tablename__ = "users"

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(120), nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(255), nullable=False)
    role       = db.Column(db.Enum("admin", "student"), default="student", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    attempts   = db.relationship("Attempt", backref="user", lazy=True)

    def set_password(self, raw):
        self.password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password, raw)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email, "role": self.role}


# ── Quiz ───────────────────────────────────────────────────────────────────────
class Quiz(db.Model):
    __tablename__ = "quizzes"

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    time_limit  = db.Column(db.Integer, default=600)   # seconds
    pass_score  = db.Column(db.Integer, default=60)    # percentage
    is_active   = db.Column(db.Boolean, default=True)
    created_by  = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    questions   = db.relationship("Question", backref="quiz", cascade="all,delete", lazy=True)
    attempts    = db.relationship("Attempt",  backref="quiz", lazy=True)

    def to_dict(self, include_questions=False):
        d = {
            "id": self.id, "title": self.title,
            "description": self.description, "time_limit": self.time_limit,
            "pass_score": self.pass_score, "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "question_count": len(self.questions),
        }
        if include_questions:
            d["questions"] = [q.to_dict() for q in self.questions]
        return d


# ── Question ───────────────────────────────────────────────────────────────────
class Question(db.Model):
    __tablename__ = "questions"

    id         = db.Column(db.Integer, primary_key=True)
    quiz_id    = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    text       = db.Column(db.Text, nullable=False)
    points     = db.Column(db.Integer, default=1)
    order_num  = db.Column(db.Integer, default=0)

    options    = db.relationship("Option", backref="question", cascade="all,delete", lazy=True)

    def to_dict(self, include_correct=False):
        return {
            "id": self.id, "text": self.text, "points": self.points,
            "order_num": self.order_num,
            "options": [o.to_dict(include_correct) for o in self.options],
        }


# ── Option ─────────────────────────────────────────────────────────────────────
class Option(db.Model):
    __tablename__ = "options"

    id          = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    text        = db.Column(db.String(500), nullable=False)
    is_correct  = db.Column(db.Boolean, default=False)

    def to_dict(self, include_correct=False):
        d = {"id": self.id, "text": self.text}
        if include_correct:
            d["is_correct"] = self.is_correct
        return d


# ── Attempt ────────────────────────────────────────────────────────────────────
class Attempt(db.Model):
    __tablename__ = "attempts"

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    quiz_id     = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    score       = db.Column(db.Float, default=0)
    max_score   = db.Column(db.Float, default=0)
    percentage  = db.Column(db.Float, default=0)
    passed      = db.Column(db.Boolean, default=False)
    started_at  = db.Column(db.DateTime, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime)

    answers     = db.relationship("Answer", backref="attempt", cascade="all,delete", lazy=True)

    def to_dict(self):
        return {
            "id": self.id, "quiz_id": self.quiz_id, "score": self.score,
            "max_score": self.max_score, "percentage": round(self.percentage, 1),
            "passed": self.passed,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
        }


# ── Answer ─────────────────────────────────────────────────────────────────────
class Answer(db.Model):
    __tablename__ = "answers"

    id          = db.Column(db.Integer, primary_key=True)
    attempt_id  = db.Column(db.Integer, db.ForeignKey("attempts.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    option_id   = db.Column(db.Integer, db.ForeignKey("options.id"))
    is_correct  = db.Column(db.Boolean, default=False)
