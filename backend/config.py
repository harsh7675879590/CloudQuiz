import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ── Flask ──────────────────────────────────────────────────────────────────
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    # ── JWT ────────────────────────────────────────────────────────────────────
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-change-me")
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour

    # ── RDS / MySQL / SQLite ────────────────────────────────────────────────────────────
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "quizadmin")
    DB_PASS = os.getenv("DB_PASS", "QuizPass123!")
    DB_NAME = os.getenv("DB_NAME", "quizdb")

    # For local testing without RDS, we'll try SQLite if LOCAL_SQLITE is true
    if os.getenv("LOCAL_SQLITE", "true").lower() == "true":
        base_dir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(base_dir, 'quiz.db')}"
    else:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── Amazon S3 ──────────────────────────────────────────────────────────────
    S3_BUCKET        = os.getenv("S3_BUCKET", "online-quiz-frontend")
    S3_REGION        = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY   = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_KEY   = os.getenv("AWS_SECRET_ACCESS_KEY", "")

    # ── CORS ───────────────────────────────────────────────────────────────────
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
