from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    """Form for signing up users"""

    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    email = StringField('E-mail', validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField('Password', validators=[Length(min=6)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=30)])

class LoginForm(FlaskForm):
    """Form for loging in a user"""

    email = StringField('E-mail Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
