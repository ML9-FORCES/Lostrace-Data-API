# Data-API Implementation 2022 Smart India Hackathon
# Contributors Garvit Chouhan, Kaustub Dutt Pandey, Chelsi Jain

# Dependencies
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
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

# result endpoint
@app.route('/result', methods=['POST'])
def result():
  if request.method == 'POST':
    if 'img' not in request.files:
      return 'There is no file in form!'
    #.........................................
    File = request.files['img']
    Mode = bool(int(request.form.get('flag')))
    Affine = Flex_Wrapper(File,mongo,Mode)
    #.........................................
    print('Fetching New Data')
    Affine.fetch() 
    print('Encoding New Data')
    Affine.encode() 
    print('Updating Database State')
    Affine.update()
    print('Flex Searching Image')
    Affine.search()
    #.........................................
    return jsonify(Affine.res)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
