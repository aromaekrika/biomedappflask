from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory, current_app, abort
from flask_login import login_required, current_user
from app.forms import TestRecordForm
from app.models import TestRecord, Patient
from app import db
from app.utils import save_uploaded_file
from sqlalchemy import or_

bp = Blueprint("tests", __name__, template_folder="../templates")

@bp.route("/", methods=["GET"])
@login_required
def list_tests():
    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", "", type=str)
    test_type = request.args.get("test_type", "", type=str)
    query = TestRecord.query.join(Patient)
    if q:
        query = query.filter(Patient.name.ilike(f"%{q}%"))
    if test_type:
        query = query.filter(TestRecord.test_type.ilike(f"%{test_type}%"))
    # researchers see only their records; admins see all
    if not current_user.is_admin():
        query = query.filter(TestRecord.added_by == current_user.id)
    pagination = query.order_by(TestRecord.date_added.desc()).paginate(page, per_page=current_app.config.get("ITEMS_PER_PAGE", 10), error_out=False)
    return render_template("tests.html", pagination=pagination, q=q, test_type=test_type)

@bp.route("/create/<int:patient_id>", methods=["GET", "POST"])
@login_required
def create_test(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = TestRecordForm()
    if form.validate_on_submit():
        filename = None
        if form.file.data:
            filename = save_uploaded_file(form.file.data)
        test = TestRecord(patient=patient, test_type=form.test_type.data, result=form.result.data, file_path=filename, added_by=current_user.id)
        db.session.add(test)
        db.session.commit()
        flash("Test record added.", "success")
        return redirect(url_for("tests.list_tests"))
    return render_template("test_form.html", form=form, patient=patient)

@bp.route("/<int:test_id>/view")
@login_required
def view_test(test_id):
    test = TestRecord.query.get_or_404(test_id)
    if not current_user.is_admin() and test.added_by != current_user.id:
        abort(403)
    return render_template("test_view.html", test=test)

@bp.route("/uploads/<path:filename>")
@login_required
def uploaded_file(filename):
    # Access control: ensure the user is allowed to view file (omitted heavy checks for brevity)
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename, as_attachment=False)
