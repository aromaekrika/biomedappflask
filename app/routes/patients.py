from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app import db
from app.models import Patient
from app.forms import PatientForm
from app import create_app
from config import Config

bp = Blueprint("patients", __name__, template_folder="../templates")

@bp.route("/", methods=["GET"])
@login_required
def list_patients():
    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", "", type=str)
    query = Patient.query
    if q:
        query = query.filter(Patient.name.ilike(f"%{q}%"))
    pagination = query.order_by(Patient.name).paginate(page, per_page=Config.ITEMS_PER_PAGE, error_out=False)
    return render_template("patients.html", pagination=pagination, q=q)

@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_patient():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(name=form.name.data, age=form.age.data, gender=form.gender.data, contact_info=form.contact_info.data)
        db.session.add(patient)
        db.session.commit()
        flash("Patient created.", "success")
        return redirect(url_for("patients.list_patients"))
    return render_template("patient_form.html", form=form)

@bp.route("/<int:patient_id>/edit", methods=["GET", "POST"])
@login_required
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = PatientForm(obj=patient)
    if form.validate_on_submit():
        form.populate_obj(patient)
        db.session.commit()
        flash("Patient updated.", "success")
        return redirect(url_for("patients.list_patients"))
    return render_template("patient_form.html", form=form, patient=patient)

@bp.route("/<int:patient_id>/delete", methods=["POST"])
@login_required
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    flash("Patient deleted.", "info")
    return redirect(url_for("patients.list_patients"))
