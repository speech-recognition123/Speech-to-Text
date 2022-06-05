from distutils.log import debug
from datetime import datetime
from pickle import load
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from flask import Flask, jsonify, make_response, request
import os


#Initialize App
app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)