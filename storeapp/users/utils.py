from flask import url_for
from flask_mail import Message
from storeapp import mail
from flask import current_app
import secrets,os
from PIL import Image

def send_confirmation_email(user):
    token = user.get_confirm_token()
    print("the token is",token)
    msg = Message('Email Confirmation', sender='youngman@gmail.com', recipients=[user.email])
    print(msg)
    msg.body = f'''To confirm you account, visit the following link:
                    {url_for('users.confirm_mail', token=token, _external=True)}
                    '''             
    mail.send(msg)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='youngman@gmail.com', recipients=[user.email])
    msg.body = f'''To reset the password to your account, visit the following link:
                    {url_for('users.reset_token', token=token, _external=True)}
                    '''             
    mail.send(msg)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static/uploads/user-profiles/', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
    

