from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import User

bp = Blueprint('admin', __name__)

@bp.route('/admin')
def index():
    pass

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('admin.login'))

        user = User.query.filter_by(username=username).first()
        if user and user.validate_password(password):
            login_user(user)
            # flash('Logged in successfully.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('admin.login'))
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    # flash('You have been logged out.')
    return redirect(url_for('index'))