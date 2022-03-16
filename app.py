from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
import tempfile
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
load_dotenv()
from Flex_Search import *


app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)
CORS = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#hhh
def before_request():
    app.jinja_env.cache = {}
app.before_request(before_request)



@app.route('/result', methods=['GET', 'POST'])
def result():
  if request.method == 'POST':
    if 'img' not in request.files:
      return 'there is no file1 in form!'
    File = request.files['img']
    format = '.'+File.filename.split('.')[-1]
    temp = tempfile.NamedTemporaryFile(suffix=format)
    File.save(temp.name)
    flag = bool(int(request.form.get('flag')))
    db=Database(mongo,flag)
    print('Retriving Database')
    db.get()
    print('Fetching Updates')
    db.fetch()
    print('Encoding Vectors')
    db.encode()
    print('Updating Database')
    db.push()
    print('Flex_Searching')
    res=Flex_Search().find(temp.name,db.data,db.vector)
    temp.close()
    return jsonify(res)


# init
if __name__ == '__main__':
    app.run(debug=True)
