from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Lost and Found API is running"
