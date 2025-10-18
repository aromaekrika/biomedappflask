from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app.forms import ReportForm
from app.models import Report, Patient
from app import db

bp = Blueprint("reports", __name__, template_folder="../templates")

@bp.route("/", methods=["GET"])
@login_required
def list_reports():
    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", "", type=str)
    query = Report.query.join(Patient)
    if q:
        query = query.filter(Patient.name.ilike(f"%{q}%"))
    if not current_user.is_admin():
        # researchers: show reports for patients that have test records created by them
        # (simple policy — adjust to your needs)
        query = query  # for now show all reports to everyone - restrict if needed
    pagination = query.order_by(Report.created_at.desc()).paginate(page, per_page=10, error_out=False)
    return render_template("reports.html", pagination=pagination, q=q)

@bp.route("/create/<int:patient_id>", methods=["GET", "POST"])
@login_required
def create_report(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = ReportForm()
    if form.validate_on_submit():
        report = Report(patient=patient, summary=form.summary.data, recommendation=form.recommendation.data)
        db.session.add(report)
        db.session.commit()
        flash("Report saved.", "success")
        return redirect(url_for("reports.list_reports"))
    return render_template("report_form.html", form=form, patient=patient)

@bp.route("/<int:report_id>/view")
@login_required
def view_report(report_id):
    report = Report.query.get_or_404(report_id)
    return render_template("report_view.html", report=report)

# PDF export placeholder (use WeasyPrint)
@bp.route("/<int:report_id>/export_pdf")
@login_required
def export_report_pdf(report_id):
    report = Report.query.get_or_404(report_id)
    # Example: render template to HTML and convert to PDF (WeasyPrint / pdfkit)
    from flask import render_template, make_response
    html = render_template("report_pdf.html", report=report)
    try:
        from weasyprint import HTML
        pdf = HTML(string=html).write_pdf()
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=report_{report.id}.pdf'
        return response
    except Exception:
        flash("PDF export not available (WeasyPrint not installed).", "warning")
        return redirect(url_for("reports.view_report", report_id=report.id))
