from flask_mail import Message, Mail
from flask import render_template
from flask import current_app as app

mail = Mail()


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(message=msg)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Mercuri] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('emails/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('emails/reset_password.html',
                                         user=user, token=token))
