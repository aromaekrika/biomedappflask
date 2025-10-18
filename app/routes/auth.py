from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import RegistrationForm, LoginForm
from app.models import User
from app import db
from flask_login import login_user, logout_user, current_user, login_required

bp = Blueprint("auth", __name__, template_folder="../templates")

@bp.route("/register", methods=["GET", "POST"])
@login_required
def register():
    # Only admins can create users
    if not current_user.is_admin():
        flash("Only admins can create users.", "warning")
        return redirect(url_for("dashboard"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("User created.", "success")
        return redirect(url_for("dashboard"))
    return render_template("register.html", form=form)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard"))
        flash("Invalid username or password", "danger")
    return render_template("login.html", form=form)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("auth.login"))
