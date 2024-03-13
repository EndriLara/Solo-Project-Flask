from flask_app import app
from flask import render_template, request, session, redirect, flash,jsonify
from flask_bcrypt import Bcrypt 
from flask_app.models.owner import Owner
from flask_app.models.car import Car
from flask_app.models.renter import Renter
bcrypt = Bcrypt(app)

from datetime import datetime
from urllib.parse import unquote
UPLOAD_FOLDER = 'flask_app/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import os
from werkzeug.exceptions import RequestEntityTooLarge

from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from werkzeug.exceptions import HTTPException, NotFound
import urllib.parse

import smtplib


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/owner/cars/new')
def newCar():
    if 'owner_id' not in session:
        return redirect('/carOwner')
    
    owner_data = {
        'owner_id': session['owner_id']
    }
    
    owner = Owner.get_owner_by_id(owner_data)
    
    if owner is None:
        return redirect('/carOwner')
    
    return render_template('newCar.html', loggedOwner=owner)


@app.route('/owner/cars/create', methods = ['POST'])
def createCar():
    if 'owner_id' not in session:
        return redirect('/carOwner')
    if not Car.validate_car(request.form):
        return redirect(request.referrer)
    if 'images' not in request.files:
        flash('Please upload an image', 'imagesCar')
        return redirect(request.referrer)
    carImages = request.files.getlist('images')
    image_filenames = []
    for carimage in carImages:
        if not allowed_file(carimage.filename):
            flash('The file should be in png, jpg or jpeg format!', 'imagesCar')
            return redirect(request.referrer)
    
        if carimage:
            filename1 = secure_filename(carimage.filename)
            time = datetime.now().strftime("%d%m%Y%S%f")
            time += filename1
            filename1 = time
            carimage.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            image_filenames.append(filename1)
            
    images_string = ','.join(image_filenames)
            
        
    data = {
        'type': request.form['type'],
        'address': request.form['address'],
        'rent': request.form['rent'],
        'description': request.form['description'],
        'images': images_string,
        'owner_id': session['owner_id']
    }
    Car.create(data)
    return redirect('/carOwner')
    

@app.route('/owner/cars/<int:id>')
def showOneCar(id):
    owner_id = session.get('owner_id')
    if owner_id is None:
        return redirect('/carOwner')
    data = {'owner_id': owner_id, 'id': id}
    owner = Owner.get_owner_by_id(data)
    if owner is None:
        return redirect('/carOwner')
    car = Car.get_car_by_id(data)
    if car is None:
        return redirect('/carOwner')
    return render_template('ownerCar.html', car=car, loggedOwner=owner)


@app.route('/renter/cars/<int:id>')
def showOneRenterCar(id):
    if 'renter_id' not in session:
        return redirect('/')
    car = Car.get_car_by_id({'id': id})
    return render_template('renterCar.html', car=car)

@app.route('/owner/cars/delete/<int:id>')
def deleteCar(id):
    if 'owner_id' not in session:
        return redirect('/carOwner')
    data = {'id': id}
    car = Car.get_car_by_id(data)
    if car and car['owner_id'] == session['owner_id']:
        Car.deleteAllPostComments(data)
        Car.delete(data)
    return redirect('/carOwner')