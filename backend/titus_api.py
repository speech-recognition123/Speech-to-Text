from distutils.log import debug
from datetime import datetime
from pickle import load
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from flask import Flask, jsonify, make_response, request
import os


#Initialize App
app = Flask(__name__)

#Route to handle the prediction
@app.route("/predict", methods=['POST'])
def predict():
    file = request.files["file"]
    pwd = os.getcwd()
    rnn_model_path = os.path.join(pwd, "model/RNN_model.pickle")
    rnn_model = load(open(rnn_model_path, "rb"))
    prediction = rnn_model.predict(file)
    return make_response(jsonify({"success": True, "data": prediction}), 200)



if __name__ == '__main__':
    app.run(debug=True)