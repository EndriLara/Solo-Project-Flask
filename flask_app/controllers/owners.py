from flask_app import app
from flask import render_template, request, session, redirect, flash,jsonify
from flask_bcrypt import Bcrypt 
from flask_app.models.owner import Owner
from flask_app.models.car import Car
bcrypt = Bcrypt(app)

@app.route('/carOwner')
def indexowner():
    if 'owner_id' in session:
        return redirect('/owner/dashboard')
    return redirect('/logout/owner')

@app.route('/register/owner', methods = ['POST'])
def registerowner():
    if 'owner_id' in session:
        return redirect('/')
    if not Owner.validate_ownerRegister(request.form):
        return redirect(request.referrer)
    owner = Owner.get_owner_by_email(request.form)
    if owner:
        flash('This account already exists', 'ownerEmailRegister')
        return redirect(request.referrer)
    
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'phone': request.form['phone'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    session['owner_id'] = Owner.create(data)
    return redirect('/carOwner')


@app.route('/login/owner')
def loginPageowner():
    return redirect('/owner/dashboard') if 'owner_id' in session else render_template('ownerLoginRegister.html')


@app.route('/login/owner', methods = ['POST'])
def loginowner():
    if 'owner_id' in session:
        return redirect('/carOwner')
    if not Owner.validate_owner(request.form):
        return redirect(request.referrer)
    owner = Owner.get_owner_by_email(request.form)
    if not owner:
        flash('This email doesnt exist', 'ownerEmailLogin')
        return redirect(request.referrer)
    
    if not bcrypt.check_password_hash(owner['password'], request.form['password']):
        flash('Incorrect password', 'ownerPasswordLogin')
        return redirect(request.referrer)
    
    session['owner_id']= owner['id']
    return redirect('/carOwner')


@app.route('/logout/owner')
def logoutOwner():
    session.clear(); return redirect('/login/owner')

@app.route('/owner/dashboard')
def dashboardOwner():
    if 'owner_id' not in session:
        return redirect('/carOwner')
    owner_id = session['owner_id']
    data = {'id': owner_id}
    cars = Car.get_my_all(data)
    return render_template('ownerdashboard.html', loggedOwner=Owner.get_owner_by_id(data), cars=cars)
