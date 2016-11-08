from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Length, Regexp

class TwilioForm(FlaskForm):
    phone_number = StringField('Phone Number: ', [InputRequired(message = "input required"), Length(min=10, max=11, message = "insufficient length"), Regexp(r"(?<![-.])\b[0-9]+\b(?!\.[0-9])", message = "invalid format")])
    message_body = StringField('Text here: ', [InputRequired(message = "input required")])
