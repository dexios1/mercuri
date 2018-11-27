from flask import Blueprint, render_template, flash, redirect, url_for, request
from mercuri.forms.login import LoginForm
from mercuri.forms.registration import RegistrationForm
from flask_login import login_user, current_user, logout_user
from werkzeug.urls import url_parse
from mercuri.models import db
from mercuri.models.user import User
from datetime import datetime

bp = Blueprint('auth', __name__)


@bp.route('/login',  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        print("next pages is {}".format(next_page))
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign in', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering, {}. You can login in now'.format(user.username))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@bp.before_request
def before_request():
    # TODO: move me to a separate blueprint for general functions, along with datetime import
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
