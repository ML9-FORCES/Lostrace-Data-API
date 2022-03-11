from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
import requests,os
from dotenv import load_dotenv
load_dotenv()


from bs4 import BeautifulSoup
import requests
import bisect

app = Flask(__name__)
#MongoDB
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

# To run python file without re-running the flask command
def before_request():
    app.jinja_env.cache = {}
app.before_request(before_request)


class Missing_ID:
  def __init__(self):
    self.db = mongo.db.Data
    self.URL = 'https://trackthemissingchild.gov.in/trackchild/photograph_missing.php?page='
    self.data = self.GET()
  #-------------------------------------------------------------
  def GET(self) :
    mydoc = self.db.find({"_id":'Unique'})
    for json in mydoc: return eval(json['Array'])
    self.db.insert_one({"_id":'Unique',"Array":[]})
    return []
  #-------------------------------------------------------------
  def SET(self):
    query = {"_id":'Unique'}
    value = {"$set":{"Array":str(self.data)}}
    self.db.update_one(query,value)
  #-------------------------------------------------------------
  def encode(self,Missing_id_str):
    s = [str(i) for i in Missing_id_str.split(".")]
    Missing_id_int = int("".join(s))
    return Missing_id_int
  #-------------------------------------------------------------
  def decode(self,Missing_id_int):
    s = str(Missing_id_int)
    substrings = [s[:2],s[2:4],s[4:6],s[6:8],s[8:10],s[10:12],s[12:14],s[14:17],
                  s[17:20],s[20:23],s[23:25],s[25:27],s[27:29],s[29:31],s[31:33],s[33:35],s[35:37],s[37:39],s[39:]]
    Missing_id_str = '.'.join(substrings)
    return Missing_id_str
  #-------------------------------------------------------------
  def binary_search(self,ID):
    low, mid, high = 0, 0, len(self.data) - 1
    while low <= high:
        mid = (high + low) // 2
        if self.data[mid] < ID: low = mid + 1
        elif self.data[mid] > ID: high = mid - 1
        else: return True
    return False
  #-------------------------------------------------------------
  def append(self,ID):
     bisect.insort(self.data,ID)
  #-------------------------------------------------------------
  def page(self,number):
    web = requests.post(self.URL+str(number))
    soup = BeautifulSoup(web.text,'html.parser')
    achors = soup.findAll('a',class_='thumbnail')
    missing_ids = []
    for block in achors:
      value=block['value']
      age_index = value.find("Current Age : ")+14
      id_index = value.find("missing_id=")+11
      age = int((value[age_index:age_index+3].split())[0])
      ID = value[id_index:id_index+60]
      if age<18:
        missing_ids.append(self.encode(ID))
    return missing_ids
  #-------------------------------------------------------------
  def fetch(self):
    index=1
    while True:
       IDs = self.page(index)
       if IDs == [] : break
       for ID in IDs:
         if self.binary_search(ID): self.SET(); return self.data
         else: self.append(ID)
       print('rendered page : ',index)
       self.SET(); index+=1
    return self.data
       

    

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

