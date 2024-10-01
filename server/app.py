# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    # Query the earthquake by ID
    earthquake = Earthquake.query.get(id)
    
    # If earthquake is found, return its data
    if earthquake:
        earthquake_data = {
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year
        }
        return jsonify(earthquake_data), 200
    else:
        # If not found, return a 404 error with a message
        response_body = {
            'message': f'Earthquake {id} not found.'
        }
        return jsonify(response_body), 404

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    # Format the response
    quakes_data = [{
        'id': quake.id,
        'location': quake.location,
        'magnitude': quake.magnitude,
        'year': quake.year
    } for quake in earthquakes]

    response_body = {
        'count': len(quakes_data),
        'quakes': quakes_data
    }

    return jsonify(response_body), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
