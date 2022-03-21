# Data-API Implementation 2022 Smart India Hackathon
# Contributors Garvit Chouhan, Kaustub Dutt Pandey, Chelsi Jain

"""  
-------------------------------------------------------------------------------
Data-API Documentation                                                        |
-------------------------------------------------------------------------------
                                                                              |
POST /search                                                                  |
    Form-Data                                                                 |
      - Image : file                                                          |
      - Mode  : 0 ( Real-Dataset  )                                           | 
                1 ( Dummy-Dataset )                                           |
Returns                                                                       |
{ Task : URL(/state/<Task_id>) }                                              |
                                                                              |
-------------------------------------------------------------------------------
                                                                              |
GET /search/<Task_id>                                                         |
                                                                              |
Returns                                                                       |
    { 'Phase':<_>, 'Info':<_> }                                               |
    - Phase: Success      Info : Person-Details (Dictionary)                  |
    - Phase: Process      Info : Current Running Process (String)             |
    - Phase: Failure      Info : Error Message (String)                       |
                                                                              |
    * Personal-Details :                                                      |
              {                                                               |
                 Img (image_link)                                             |
                 Report_link ( Redirects to Report Page )                     |
                 Profile_link ( Redirects to Full Profile Page )              |
                 Name                                                         |
                 Current_Age                                                  |
                 Gender                                                       |
                 Father_Name                                                  |
                 Place_of_Missing                                             |
                 Date_of_Missing                                              |
               }                                                              |
                                                                              |
    * Current Running Process :                                               |
               - 'Fetching New Data'                                          |
               - 'Encoding New Data'                                          |
               - 'Updating Database State'                                    |
               - 'Flex Searching Image'                                       |
                                                                              |
    * Error Message :                                                         |	
               - 'No Image Uploaded'                                          |
               - 'No Face Detected'                                           |
               - 'Person Not Found'                                           |
                                                                              |
------------------------------------------------------------------------------- 
"""



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

#Flex-Background-Process
Flex_Process = Background_Task(mongo)


# search endpoint 
@app.route('/search', methods=['POST'])
def result():
  if request.method == 'POST':
    if 'Image' not in request.files: File = None
    else: File = request.files['Image']
    Mode = bool(int(request.form.get('Mode')))
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
