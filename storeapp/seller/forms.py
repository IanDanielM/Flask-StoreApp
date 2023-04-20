from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired,Length, Email,EqualTo,Optional,ValidationError
import email_validator
from storeapp.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username =  StringField('Username', validators=[DataRequired(),Length(min=3,max=25)])
    email=StringField('Email', validators=[Email(),DataRequired()])
    password=PasswordField('Password', validators=[DataRequired(), Length(min=5,max=25)])
    confirm_password=PasswordField('Confirm Passsword', validators=[EqualTo('password', message="Passwords must match"),DataRequired()])
    address = StringField('Address',validators=[DataRequired()])
    country = SelectField('Country', choices=[('US', 'United States'), ('UK', 'United Kingdom'), ('FR', 'France'), ('DE', 'Germany')], validators=[DataRequired()])
    town = StringField('Town',validators=[Optional()])
    submit = SubmitField('Sign Up')
   
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')
        
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists')
        

    