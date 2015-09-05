
from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired


class NewPostForm(Form):
    name = StringField(validators=[DataRequired()])
    comment = TextAreaField()


class NewThreadForm(NewPostForm):
    subject = StringField(validators=[DataRequired()])