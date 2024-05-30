from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from forms import RegistrationForm, LoginForm, PatientForm, AppointmentForm
from models import db, User, Patient, Appointment
import joblib
import pandas as pd
from datetime import datetime
import config

app = Flask(__name__)
app.config.from_object(config.Config)

db.init_app(app)
#db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

# Load the model
model = joblib.load('no_show_predictor.joblib')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

@app.route('/add_patient', methods=['GET', 'POST'])
@login_required
def add_patient():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(name=form.name.data, age=form.age.data, address=form.address.data)
        db.session.add(patient)
        db.session.commit()
        flash('Patient has been added!', 'success')
        return redirect(url_for('view_patients'))
    return render_template('add_patient.html', title='Add Patient', form=form)

@app.route('/view_patients')
@login_required
def view_patients():
    patients = Patient.query.all()
    return render_template('view_patients.html', title='View Patients', patients=patients)

@app.route('/add_appointment', methods=['GET', 'POST'])
@login_required
def add_appointment():
    form = AppointmentForm()
    if form.validate_on_submit():
        appointment = Appointment(patient_id=form.patient_id.data, date=form.date.data, time=form.time.data, reason=form.reason.data)
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment has been scheduled!', 'success')
        return redirect(url_for('view_appointments'))
    return render_template('add_appointment.html', title='Add Appointment', form=form)


@app.route('/view_appointments')
@login_required
def view_appointments():
    appointments = db.session.query(Appointment, Patient).join(Patient, Appointment.patient_id == Patient.id).all()
    return render_template('view_appointments.html', title='View Appointments', appointments=appointments)

def create_tables():
    with app.app_context():
        db.create_all()


@app.route('/predictions')
@login_required
def predictions():
    # Query appointments and their related patients
    appointments = db.session.query(Appointment, Patient).join(Patient, Appointment.patient_id == Patient.id).all()
    return render_template('predictions.html', title='Predict No-Show', appointments=appointments)


    
@app.route('/edit_patient/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_patient(id):
    patient = Patient.query.get_or_404(id)
    form = PatientForm()
    if form.validate_on_submit():
        patient.name = form.name.data
        patient.age = form.age.data
        patient.address = form.address.data
        db.session.commit()
        flash('Patient details have been updated!', 'success')
        return redirect(url_for('view_patients'))
    elif request.method == 'GET':
        form.name.data = patient.name
        form.age.data = patient.age
        form.address.data = patient.address
    return render_template('edit_patient.html', title='Edit Patient', form=form)


@app.route('/delete_patient/<int:id>', methods=['POST'])
@login_required
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient has been deleted!', 'success')
    return redirect(url_for('view_patients'))

@app.route('/edit_appointment/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    form = AppointmentForm(obj=appointment)
    if form.validate_on_submit():
        form.populate_obj(appointment)
        db.session.commit()
        flash('Appointment details have been updated!', 'success')
        return redirect(url_for('view_appointments'))
    elif request.method == 'GET':
        form.patient_id.data = appointment.patient_id
        form.date.data = appointment.date
        form.time.data = appointment.time
        form.reason.data = appointment.reason
    return render_template('edit_appointment.html', title='Edit Appointment', form=form)



@app.route('/delete_appointment/<int:id>', methods=['POST'])
@login_required
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    flash('Appointment has been deleted!', 'success')
    return redirect(url_for('view_appointments'))



if __name__ == '__main__':
    create_tables()
    app.run(debug=True)