import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from login import  mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,'static/profile_pics',picture_fn)
    form_picture.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg= Message('Password Reset Request',sender='smk3596@gmail.com',recipients=[user.email])
    msg.body=f'''To reset your password, visit the following link:
    {url_for('users.reset_token',token=token,_external=True)}

    If you did not make this request then just ignore this mail.
    '''
    mail.send(msg)
