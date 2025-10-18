import os
from werkzeug.utils import secure_filename
from flask import current_app
from functools import wraps
from flask_login import current_user
from flask import abort

def allowed_file(filename):
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in current_app.config["ALLOWED_EXTENSIONS"]

def save_uploaded_file(file_storage):
    if file_storage and allowed_file(file_storage.filename):
        filename = secure_filename(file_storage.filename)
        # ensure uploads folder exists
        os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
        dst = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        # if collision, add suffix
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(dst):
            filename = f"{base}_{counter}{ext}"
            dst = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            counter += 1
        file_storage.save(dst)
        return filename
    return None

def admin_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return wrapped
