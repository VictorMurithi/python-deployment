# app.py

import os
from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Bird

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize the db and migrate
db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)

class Birds(Resource):
    def get(self):
        try:
            birds = [bird.to_dict() for bird in Bird.query.all()]
            return make_response(jsonify(birds), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)


class BirdByID(Resource):
    def get(self, id):
        bird = Bird.query.filter_by(id=id).first()

        if bird:
            return make_response(jsonify(bird.to_dict()), 200)
        else:
            return make_response(jsonify({'error': 'Bird not found'}), 404)


@app.route('/')
def index():
    return 'Bird App'
