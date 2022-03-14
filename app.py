from flask import Flask, render_template, jsonify,request
from flask_pymongo import PyMongo
import requests,os
from dotenv import load_dotenv
load_dotenv()


from bs4 import BeautifulSoup
import requests
import bisect

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

# To run python file without re-running the flask command
def before_request():
    app.jinja_env.cache = {}
app.before_request(before_request)

      
db = Database(mongo)
MissingID = Missing_ID(db)

# Routes
@app.route('/result')
def result():
  res={
  "Img" : "https://trackthemissingchild.gov.in/trackchild/intra_trackchild/images_missing/3281805mpw20220010.jpg",
  "Name" : "PANCHANU KUMAR RAJAK",
  "Current_Age" : "17 Years 0 Months 6 Days",
  "Gender" : "MALE",
  "Father_Name" : "BHUDEB RAJAK",
  "Place_of_Missing" : "SREEBHUMI",
  "Date_of_Missing" : "10/03/2022",
  "Profile_link" : "https://trackthemissingchild.gov.in/trackchild/missing_dtl.php?		missing_id=47.46.52.45.52.44.49.105.108.115.46.44.46.46.44.44.45.44.102#verticalTab1",
  "Report_link" : "https://trackthemissingchild.gov.in/trackchild/photograph_info_ps.php?profile_no=3281805mpw20220010&return_page=photograph_missing.php&type=missing&authority=1"  
  }
  return jsonify(res)

  

# init
if __name__ == '__main__':
    app.run(debug=True)

