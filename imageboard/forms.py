
from flask_wtf import Form
from wtforms.fields import StringField, FileField
from wtforms.validators import DataRequired


class NewPostForm(Form):
    name = StringField(default='Anonymous', validators=[DataRequired()])
    comment = StringField()


class NewThreadForm(NewPostForm):
    subject = StringField(validators=[DataRequired()])