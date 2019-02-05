from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from flask_babel import _, lazy_gettext as _l
from app.models import User



class TaskForm(FlaskForm):
	summary= StringField(_l('Summarize your Problem'), validators=[DataRequired()])
	body= StringField(_l('Descripe your Problem'), validators=[DataRequired()])
	internet= StringField(_l('Does the Device still have access to the Internet?'), validators=[DataRequired()])
	tags= StringField(_l('Username'), validators=[DataRequired()])
	create = SubmitField(_l('Create'))