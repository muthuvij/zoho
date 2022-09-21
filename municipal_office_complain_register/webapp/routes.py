from webapp import app
from flask import render_template, redirect, url_for, flash, request
from webapp.models import Complaint, User
from webapp.forms import RegisterForm, LoginForm, ComplaintForm, ApproveForm, DisapproveForm, TakeActionForm, SolveIssueForm, SearchComplaintCitizenForm
from webapp import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/view_complaints', methods=['GET', 'POST'])
@login_required
def view_complaints_page():
    disapprove_form = DisapproveForm()
    approve_form = ApproveForm()
    if request.method == "POST":
        approved_complaint = request.form.get('approved_complaint')
        if approved_complaint:
            complaint = Complaint.query.filter_by(id=approved_complaint).first()
            complaint.approved()
            flash("Complaint approved successfully!", category='Info')
        disapproved_complaint = request.form.get('disapproved_complaint')
        if disapproved_complaint:
            if request.form.get('reason') != '':
                complaint = Complaint.query.filter_by(id=disapproved_complaint).first()
                complaint.disapproved(request.form.get('reason'))
                flash("Complaint disapproved successfully!", category='Info')
            else:
                flash("Select appropriate reason!", category='Info')
        return redirect(url_for('view_complaints_page'))

    if request.method == "GET":
        complaints = Complaint.query.filter_by(status='Pending')
        return render_template('view_complaints.html', complaints=complaints, approve_form=approve_form, disapprove_form=disapprove_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with making you an admin: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/complaint', methods=['GET', 'POST'])
def complaint_page():
    form = ComplaintForm()
    if form.validate_on_submit():
        if form.email_address.data == '':
            complaint_to_register = Complaint(name=form.name.data,
                                              address=form.address.data,
                                              phone_number=form.phone_number.data,
                                              description = form.description.data,
                                              status = 'Pending')
        else:
            complaint_to_register = Complaint(name=form.name.data,
                                              address=form.address.data,
                                              phone_number=form.phone_number.data,
                                              email_address=form.email_address.data,
                                              description=form.description.data,
                                              status = 'Pending')
        db.session.add(complaint_to_register)
        db.session.commit()
        flash(f"{complaint_to_register.name}, your complaint has been registered!",
                category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error in your entry: {err_msg}', category='danger')

    return render_template('register_complaint.html', form=form)

@app.route('/approved_complaint', methods=['GET', 'POST'])
def approved_complaints_page():
    take_action_form = TakeActionForm()
    if request.method == "POST":
        take_action = request.form.get('take_action')
        if take_action:
            complaint = Complaint.query.filter_by(id=take_action).first()
            complaint.take_action()
            flash("Thank you for taking action!", category='Info')
        return redirect(url_for('approved_complaints_page'))

    if request.method == "GET":
        complaints = Complaint.query.filter_by(status='Approved')
        return render_template('approved_complaints.html', complaints=complaints, take_action_form=take_action_form)

@app.route('/action_taken_complaint', methods=['GET', 'POST'])
def action_taken_complaints_page():
    solve_issue_form = SolveIssueForm()
    if request.method == "POST":
        solve_issue = request.form.get('solve_issue')
        if solve_issue:
            complaint = Complaint.query.filter_by(id=solve_issue).first()
            complaint.issue_solved()
            flash("Thank you for solving the issue!", category='Info')
        return redirect(url_for('action_taken_complaints_page'))

    if request.method == "GET":
        complaints = Complaint.query.filter_by(status='Action will be taken soon')
        return render_template('action_taken_complaints.html', complaints=complaints, solve_issue_form=solve_issue_form)

@app.route('/check_my_complaint', methods=['GET', 'POST'])
def check_my_complaint_page():
    form = SearchComplaintCitizenForm()
    if request.method == "POST":
        phone_number = form.phone_number.data
        complaints = Complaint.query.filter_by(phone_number=phone_number)
        if complaints.first():
            return redirect(url_for('list_my_complaint_page', phone_number=phone_number))
        else:
            flash(f"No complaints registered in the {phone_number} - phone number", category='danger')
            return redirect(url_for('check_my_complaint_page'))

    if request.method == "GET":
        return render_template('check_my_complaints.html', form=form)

@app.route('/list_my_complaint/<phone_number>/', methods=['GET'])
def list_my_complaint_page(phone_number):
    complaints = Complaint.query.filter_by(phone_number=phone_number)
    if complaints.first():
        return render_template('list_my_complaint.html', keys=phone_number, complaints=complaints)
    else:
        flash(f"No complaints registered in the {phone_number} - phone number", category='danger')
        return redirect(url_for('check_my_complaint_page'))