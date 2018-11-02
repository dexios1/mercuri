from flask import Blueprint, render_template, flash, redirect, url_for
from mercuri.forms.login import LoginForm

bp = Blueprint('auth', __name__)


@bp.route('/login',  methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('auth/login.html', title='Sign in', form=form)


@bp.route('/register')
def register():
    pass
