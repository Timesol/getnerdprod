from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField,SelectField,RadioField,SelectMultipleField,HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length,InputRequired
from flask_babel import _, lazy_gettext as _l
from app.models import User
from wtforms.widgets import ListWidget, CheckboxInput



class MultiCheckboxField(SelectMultipleField):
    widget          = ListWidget(prefix_label=False)
    option_widget   = CheckboxInput()




class TaskForm(FlaskForm):
    summary= StringField(_l('Summarize your Problem'), validators=[DataRequired()])
    body= TextAreaField(_l('Describe your Problem'), validators=[DataRequired()], id='body-add-task')
    internet=BooleanField(_l('Does the Device still have access to the Internet?'), render_kw={'data-toggle':'toggle','data-on':'Yes' ,'data-off':'No'}, id='internet-toogle')
    tags= StringField(_l('Categorys'), render_kw={'data-toggle':'modal', 'data-target':'#modal-tags1'})
    city=SelectField(u'City', coerce=int, validators=[InputRequired()])
    price=StringField(_l('Price'), validators=[DataRequired()])
    currency=SelectField(_l('Currency'),
        choices=[('&#128;', '€'),('&#36;', '$'), ('&#163;','£')])
    methods=MultiCheckboxField(_l('How can you reach me'),  choices=[('telefon','Telefon'), ('app','Foxonauts App'),('whats','Whatsapp'),('email','Email')])
    create = SubmitField(_l('Create'))
    folder_name=HiddenField(render_kw={'data-string':'not_set'})


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))