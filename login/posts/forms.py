from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    name = StringField('Title',validators=[DataRequired()])
    author= TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Post')
