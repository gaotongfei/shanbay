from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange


class SignupForm(Form):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('submit')


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember me')
    submit = SubmitField('submit')


class SettingsForm(Form):
    words_per_day = IntegerField('words per day', validators=[DataRequired(), NumberRange(1, 100)])
    category = SelectField('category', choices=[('cet4', 'cet4'), ('cet6', 'cet6'), ('toefl', 'toefl')])
    submit = SubmitField('submit')
