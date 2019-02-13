from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField,SelectField,RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length,InputRequired
from flask_babel import _, lazy_gettext as _l
from app.models import User



class TaskForm(FlaskForm):
	summary= StringField(_l('Summarize your Problem'), validators=[DataRequired()])
	body= TextAreaField(_l('Describe your Problem'), validators=[DataRequired()], id='body-add-task')
	internet=BooleanField(_l('Does the Device still have access to the Internet?'), render_kw={'data-toggle':'toggle','data-on':'Yes' ,'data-off':'No'}, id='internet-toogle')
	tags= StringField(_l('Tags'), validators=[DataRequired()], render_kw={'data-toggle':'modal', 'data-target':'#modal-tags1'})
	city=SelectField(u'City', coerce=int, validators=[InputRequired()])
	price=StringField(_l('Price'), validators=[DataRequired()])
	currency=SelectField(_l('Currency'),
        choices=[('euro', '€'),('dollar', '$'), ('pfund','£')])
	create = SubmitField(_l('Create'))