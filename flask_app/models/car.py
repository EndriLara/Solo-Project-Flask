from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

class Car:
    db_name = "rentdb"
    def __init__(self, data):
        self.id = data['id']
        self.type = data['type']
        self.address = data['address']
        self.rent = data['rent']
        self.description = data['description']
        self.images = data.get('images', [])
        self.owner_id = data['owner_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def create(cls, data):
        query = "INSERT INTO cars (type, address, rent, description, images, owner_id) VALUES (%(type)s, %(address)s, %(rent)s, %(description)s, %(images)s, %(owner_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cars;"
        results = connectToMySQL(cls.db_name).query_db(query)
        cars = []
        if results:
            for car in results:
                cars.append(car)
            return cars
        return cars
    
    @classmethod
    def get_my_all(cls, data):
        query = "SELECT * FROM cars where owner_id = %(id)s;"
        cars = connectToMySQL(cls.db_name).query_db(query, data)
        return cars or []
    
    @classmethod
    def get_car_by_id(cls, data):
        query = 'SELECT * FROM cars left join owners on cars.owner_id = owners.id where cars.id = %(id)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            query2 = 'SELECT * FROM comments left join renters on comments.renter_id = renters.id WHERE comments.car.id = %(id)s;'
            results2 =  connectToMySQL(cls.db_name).query_db(query2, data)
            comments = []
            if results2:
                for comment in results2:
                    comments.append(comment)
            result[0]['comments'] = comments
            return result[0]
        return False
    

    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM cars where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @classmethod
    def updateCar(cls, data):
        query = "UPDATE cars set type=%(type)s, address = %(address)s, rent = %(rent)s, description = %(description)s, images = %(images)s where cars.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_car(car):
        is_valid = True
        
        if len(car['type'])<1:
            flash("Type of car is required!", 'typeCar')
            is_valid = False
        if len(car['address'])<3:
            flash("Address is required!", 'addressCar')
            is_valid = False
        if len(car['description'])<3:
            flash("Description for the car is required!", 'descriptionCar')
            is_valid = False
        if len(car['rent'])<1:
            flash("Rent is required!", 'rentCar')
            is_valid = False

        return is_valid
    
    @staticmethod
    def validate_carComment(comment):
        is_valid = True
        if len(comment['comment'])< 2:
            flash('comment should be more  or equal to 2 characters', 'renterCommentCar')
            is_valid = False
        return is_valid