from distutils.log import debug
from datetime import datetime
from pickle import load
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from flask import Flask, jsonify, make_response, request
import os


#Initialize App
app = Flask(__name__)

base_dir = os.path.dirname(__file__)

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(base_dir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init DB
db = SQLAlchemy(app)

#Init Marshmallow
ma = Marshmallow(app)

# Creating the features db
class Features(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200))
    text = db.Column(db.String(1000))
    duration = db.Column(db.String(250))

    def __init__(self, path,text, duration):
        self.path = path
        self.text = text
        self.duration = duration


#Create the database schema
class FeatureSchema(ma.Schema):
    class Meta:
        fields = ['id', 'path', 'text', 'duration']

#Init Schema
feature_schema = FeatureSchema()
# products_schema = ProductSchema(many=True,)


#Route to handle the prediction
@app.route('/predict', methods=['POST', 'GET'])
def predict():
    #Filtering details from received json file and processing
    path = request.json['path']
    text = request.json['text']
    duration = request.json['duration']

    new_file = Features(path,text, duration)
    db.session.add(new_file)
    db.session.commit()

    file = {"path": path,
            "text": text,
            "duration": duration}
    
    # pwd = os.getcwd()
    # rnn_model_path = os.path.join(pwd, "../model/RNN_model.pickle")
    # rnn_model = load(open(rnn_model_path, "rb"))
    # prediction = rnn_model.predict(file)

    return jsonify(file)



if __name__ == '__main__':
    app.run(debug=True)