from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

class PatientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    age = IntegerField('Age', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=200)])
    submit = SubmitField('Add Patient')

class AppointmentForm(FlaskForm):
    patient_id = IntegerField('Patient ID', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    time = TimeField('Time', validators=[DataRequired()])
    reason = StringField('Reason', validators=[DataRequired(), Length(min=5, max=200)])
    submit = SubmitField('Schedule Appointment')

