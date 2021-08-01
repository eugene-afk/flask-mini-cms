from flask import Blueprint, render_template, redirect, url_for, request, flash, Markup
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    return render_template('login.html')

@auth.route('/login',methods=['POST'])
def login_post():
    try:
        name = request.form.get('name')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(name=name).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your credentials and try again.')
            flash('danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** login_post msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/changepassword')
@login_required
def change_password():
    return render_template('change_password.html')

@auth.route('/changepassword', methods=['POST'])
@login_required
def change_password_post():
    try:
        old_pw = request.form.get('old_password')
        new_pw = request.form.get('new_password')
        repeat_new_pw = request.form.get('repeat_new_password')
        
        if new_pw != repeat_new_pw:
            flash('New passwords mismatch.')
            flash('danger')
            return redirect(url_for('auth.change_password'))

        user = User.query.filter_by(id=current_user.id).first()
        if not check_password_hash(user.password, old_pw):
            flash('Wrong password.')
            flash('danger')
            return redirect(url_for('auth.change_password'))

        user.password = generate_password_hash(new_pw, method='sha256')
        db.session.commit()

        logout_user()
        flash('Password changed. Login with new password.')
        flash('success')
        return redirect(url_for('auth.login'))
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** change_password_post msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))