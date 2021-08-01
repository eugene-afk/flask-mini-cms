from flask import Blueprint, render_template, redirect, request, url_for, flash, Markup
from flask_login import login_required
from .models import User
from . import db
from flask import Markup
from werkzeug.security import generate_password_hash
from datetime import datetime

users = Blueprint('users', __name__)

@users.route('/duser/<id>', methods=['GET', 'POST'])
@login_required
def duser(id):
    try:
        if int(id) == 1:
            flash(Markup('You can not delete this user!'))
            flash('danger')
            return redirect(url_for('main.users'))

        usr = User.query.filter_by(id=id).first()
        name = usr.name
        db.session.delete(usr)
        db.session.commit()
        flash(Markup('User <strong>' + str(name) + '</strong> was deleted!'))
        flash('success')
        return redirect(url_for('main.users'))
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** duser msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))

@users.route('/adduser', methods=['POST'])
@login_required
def adduser_post():
    try:
        email = request.form.get('email')
        name = request.form.get('name')
        user = User.query.filter_by(email=email).first()
        if user:
            flash(Markup('Email address <strong>' + email + '</strong> already exists'))
            return redirect(url_for('main.users'))
        user = User.query.filter_by(email=email).first()
        if user:
            flash(Markup('Name <strong>' + name + '</strong> already exists'))
            flash('danger')
            return redirect(url_for('main.users'))

        password = request.form.get('password')

        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()

        flash(Markup('User <strong>' + new_user.name + '</strong> was succussfully added!<br/>'+
                    '<div id="copy_creds" class="pointer">Copy to clipboard</div>' +
                    '<div id="show_pwd" class="pointer">Show password</div>' +
                    '<div id="creds" style="display: none;"><input id="sname" type="hidden" name="sname" value="' + new_user.name + '">' +
                    '<input disabled id="spassword" type="hidden" name="spassword" value="' + password + '"></div>'))
        flash('success')
        return redirect(url_for('main.users')) 
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** adduser_post msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))

@users.route('/adduser')
@login_required
def adduser():
    return render_template('adduser.html')

