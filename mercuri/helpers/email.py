from flask_mail import Message, Mail
from flask import render_template
from flask import current_app
from threading import Thread

mail = Mail()


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    app = current_app._get_current_object()
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user, app_url=None):
    token = user.get_reset_password_token()
    send_email('[Mercuri] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('emails/reset_password.txt',
                                         user=user, token=token, app_url=app_url),
               html_body=render_template('emails/reset_password.html',
                                         user=user, token=token, app_url=app_url))
