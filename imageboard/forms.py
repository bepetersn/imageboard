
from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField, FileField
from wtforms.validators import InputRequired


class NewPostForm(Form):
    name = StringField(validators=[InputRequired()])
    comment = TextAreaField()
    image = FileField()


class NewThreadForm(NewPostForm):
    subject = StringField(validators=[InputRequired()])
    image = FileField(validators=[InputRequired()])