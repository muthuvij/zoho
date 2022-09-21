from webapp import db, login_manager
from webapp import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Complaint(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    address = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(), nullable=False)
    email_address = db.Column(db.String(), default=None)
    description = db.Column(db.String(length=1024), nullable=False)
    status = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'Complaint {self.name}'

    def approved(self):
        self.status = 'Approved'
        db.session.commit()

    def disapproved(self, reason):
        self.status = f'Disapproved - {reason}'
        db.session.commit()

    def take_action(self):
        self.status = 'Action will be taken soon'
        db.session.commit()

    def issue_solved(self):
        self.status = 'Issue Solved'
        db.session.commit()