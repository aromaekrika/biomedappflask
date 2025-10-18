from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, NumberRange
from flask_wtf.file import FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(3, 80)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    role = SelectField("Role", choices=[("researcher", "Researcher"), ("admin", "Admin")])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class PatientForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(1, 140)])
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=0, max=150)])
    gender = SelectField("Gender", choices=[("", "Choose..."), ("Male", "Male"), ("Female", "Female"), ("Other", "Other")])
    contact_info = TextAreaField("Contact Info", validators=[Optional(), Length(max=200)])
    submit = SubmitField("Save")

class TestRecordForm(FlaskForm):
    test_type = StringField("Test Type", validators=[DataRequired(), Length(max=120)])
    result = TextAreaField("Result", validators=[Optional(), Length(max=5000)])
    file = FileField("Attach file", validators=[FileAllowed(["pdf", "png", "jpg", "jpeg"], "PDFs/images only!")])
    submit = SubmitField("Save")

class ReportForm(FlaskForm):
    summary = TextAreaField("Summary", validators=[DataRequired(), Length(max=10000)])
    recommendation = TextAreaField("Recommendation", validators=[Optional(), Length(max=5000)])
    submit = SubmitField("Create Report")
