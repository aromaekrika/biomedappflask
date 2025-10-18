from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # Blueprints
    from app.routes.auth import bp as auth_bp
    from app.routes.patients import bp as patients_bp
    from app.routes.tests import bp as tests_bp
    from app.routes.reports import bp as reports_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(patients_bp, url_prefix="/patients")
    app.register_blueprint(tests_bp, url_prefix="/tests")
    app.register_blueprint(reports_bp, url_prefix="/reports")

    # main routes (dashboard)
    @app.route("/")
    def index():
        from flask import redirect, url_for
        return redirect(url_for("dashboard"))

    from flask import render_template
    @app.route("/dashboard")
    def dashboard():
        # lightweight dashboard stats
        from app.models import Patient, TestRecord, Report
        patients_count = Patient.query.count()
        tests_count = TestRecord.query.count()
        reports_count = Report.query.count()
        recent_reports = Report.query.order_by(Report.created_at.desc()).limit(5).all()
        return render_template("dashboard.html", patients_count=patients_count,
                               tests_count=tests_count, reports_count=reports_count,
                               recent_reports=recent_reports)

    return app
