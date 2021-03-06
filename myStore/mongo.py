
#from app import app
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

#app.config['MONGO_URI'] = 'mongodb://<user>:<password>@<url>:27017/dev?authSource=admin'


app.config['MONGO_URI'] = 'mongodb://localhost:27017/mykart'
mongo = PyMongo(app)


@app.route('/mongo', methods=['GET'])
def get_all_docs():
    doc = mongo.db.abcd.insert({'abcd': 'abcd'})
    return "Inserted"


if __name__ == '__main__':
    app.run(debug=True)
