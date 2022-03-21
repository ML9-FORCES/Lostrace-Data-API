# Data-API Implementation 2022 Smart India Hackathon
# Contributors Garvit Chouhan, Kaustub Dutt Pandey, Chelsi Jain

# Dependencies
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo,ObjectId
from dotenv import load_dotenv
from flask_cors import CORS
from Flex_Algo import *
import os
load_dotenv()

# Initialize Flask App
app = Flask(__name__)

# Connect MongoDB
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

# API Cross Origin Support
CORS = CORS(app)

# Runtime Catch
def before_request():
    app.jinja_env.cache = {}
app.before_request(before_request)

Flex_Process = Background_Task(mongo)

# search endpoint
@app.route('/search', methods=['POST'])
def result():
  if request.method == 'POST':
    if 'img' not in request.files: File = None
    else: File = request.files['img']
    Mode = bool(int(request.form.get('flag')))
    task = Flex_Process.run(File,Mode)
    return jsonify(task)

# state endpoint
@app.route("/state/<ObjectId:task_id>")
def state(task_id):
    res = Flex_Process.state(task_id)
    return jsonify(res)
    

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
