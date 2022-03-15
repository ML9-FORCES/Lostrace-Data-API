from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
import tempfile
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
load_dotenv()
from helpers import *


app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)
CORS = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


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
    db=Database(mongo,True)
    data,vector=db.GET()
    res=Flex_Search().find(temp.name,data,vector)
    temp.close()
    return(res)
    res = {
    "Img": "https://trackthemissingchild.gov.in/trackchild/intra_trackchild/images_missing/3281805mpw20220010.jpg",
    "Name": "PANCHANU KUMAR RAJAK",
    "Current_Age": "17 Years 0 Months 6 Days",
    "Gender": "MALE",
    "Father_Name": "BHUDEB RAJAK",
    "Place_of_Missing": "SREEBHUMI",
    "Date_of_Missing": "10/03/2022",
    "Profile_link": "https://trackthemissingchild.gov.in/trackchild/missing_dtl.php?		missing_id=47.46.52.45.52.44.49.105.108.115.46.44.46.46.44.44.45.44.102#verticalTab1",
    "Report_link": "https://trackthemissingchild.gov.in/trackchild/photograph_info_ps.php?profile_no=3281805mpw20220010&return_page=photograph_missing.php&type=missing&authority=1"
    }
    return res
    

@app.route('/test')
def test():
  db=Database(mongo,True)
  data,vector=db.GET()
  query='https://www.looper.com/img/gallery/the-transformation-of-a-j-cook-from-childhood-to-criminal-minds/intro-1616872412.jpg'
  res=Flex_Search().find(query,data,vector)
  return(res)


# init
if __name__ == '__main__':
    app.run(debug=True)
