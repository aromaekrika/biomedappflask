import os
from pathlib import Path

basedir = Path(__file__).parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or f"sqlite:///{basedir / 'biomed.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER") or str(basedir / "uploads")
    ALLOWED_EXTENSIONS = set((os.environ.get("ALLOWED_EXTENSIONS") or "pdf,png,jpg,jpeg").split(","))
    ITEMS_PER_PAGE = int(os.environ.get("ITEMS_PER_PAGE", 10))
