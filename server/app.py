#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self): 
        all = Plant.query.all()
        plants = []
        for plant in all: 
            plants.append(plant.to_dict())
        return (plants), 200
    def post(self): 
        plant = Plant()
        data = request.json
        try:
            for attr in data: 
                setattr(plant, attr, data[attr])
            db.session.add(plant)
            db.session.commit()
            return plant.to_dict, 201
        except(IntegrityError, ValueError) as ie: 
            return {'error': ie.args}, 422
    
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id): 
        plant = Plant.query.filter(Plant.id == id).first()
        return plant.to_dict(), 200
    
api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
