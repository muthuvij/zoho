from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from webapp.models import User
import re


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    def validate_secret_code(self, secret_code_to_check):
        if secret_code_to_check.data != 'cheemsforlife':
            print(secret_code_to_check.data)
            raise ValidationError("Secret code doesn't match")

    username = StringField(label='Admin Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    secret_code = PasswordField(label='Secret Code:', validators=[DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='Admin Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class ComplaintForm(FlaskForm):
    def validate_name(self, name_to_check):
        if not (name_to_check.data != '' and
                all(chr.isalpha() or chr.isspace() for chr in name_to_check.data)):
            raise ValidationError('Invalid name format! Please provide your real full name')

    def validate_phone_number(self, phone_number_to_check):
        phone_number_format = "(0|91)?[7-9][0-9]{9}"
        if not re.fullmatch(phone_number_format, phone_number_to_check.data):
            raise ValidationError('Invalid phone number format! Please provide your real phone number')

    def validate_email_address(self, email_address_to_check):
        email_address_format = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not (re.fullmatch(email_address_format, email_address_to_check.data) or email_address_to_check.data == ''):
            raise ValidationError('Invalid e-mail address format! Please provide your real e-mail address or leave it blank')

    name = StringField(label='Full Name:', validators=[Length(min=2, max=30), DataRequired()])
    address = StringField(label='Address:', validators=[Length(min=6, max=100), DataRequired()])
    phone_number = StringField(label='Phone Number:', validators=[DataRequired(), Length(max=14)])
    email_address = StringField(label='Email Address:')
    description = TextAreaField(label='Description:', validators=[DataRequired()])
    submit = SubmitField(label='Register Complaint')

class ApproveForm(FlaskForm):
    submit = SubmitField(label='Approve')

class DisapproveForm(FlaskForm):
    submit = SubmitField(label='Disapprove')

class TakeActionForm(FlaskForm):
    submit = SubmitField(label='Take Action')

class SolveIssueForm(FlaskForm):
    submit = SubmitField(label='Issue Solved')

class SearchComplaintCitizenForm(FlaskForm):
    phone_number = StringField(label='Phone Number:', validators=[DataRequired(), Length(max=14)])
    submit = SubmitField(label='Search')