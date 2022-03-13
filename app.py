from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
load_dotenv()


app = Flask(__name__)
CORS = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# MongoDB
# app.config["MONGO_URI"] = os.getenv("MONGO_URI")
# mongo = PyMongo(app)

# To run python file without re-running the flask command


def before_request():
    app.jinja_env.cache = {}


app.before_request(before_request)


# class Database:
#   def __init__(self):
#     self.db = mongo.db.Data
#   #-------------------------------------------------------------
#   def GET(self,ID) :
#     mydoc = self.db.find({"_id":ID})
#     for json in mydoc: return json['Array']
#     self.db.insert_one({"_id":ID,"Array":[]})
#     return []
#  #-------------------------------------------------------------
#   def SET(self,ID,VALUE):
#     query = {"_id":ID}
#     value = {"$set":{"Array":VALUE}}
#     self.db.update_one(query,value)

# class Missing_ID:
#   def __init__(self):
#     self.db = Database()
#     self.URL = 'https://trackthemissingchild.gov.in/trackchild/photograph_missing.php?page='
#     self.data = self.db.GET('data')
#   #-------------------------------------------------------------
#   def page(self,number):
#     web = requests.post(self.URL+str(number))
#     soup = BeautifulSoup(web.text,'html.parser')
#     achors = soup.findAll('a',class_='thumbnail')
#     missing_ids = []
#     for block in achors:
#       value=block['value']
#       age_index = value.find("Current Age : ")+14
#       id_index = value.find("missing_id=")+11
#       Profile_no_index = value.find("profile_no=")+11
#       age = int((value[age_index:age_index+3].split())[0])
#       ID = value[id_index:id_index+60]
#       Profile_no = value[Profile_no_index:Profile_no_index+18]
#       if age<18:
#         missing_ids.append([ID,Profile_no])
#     return missing_ids
#   #-------------------------------------------------------------
#   def fetch(self,index=1):
#     while True:
#        IDs = self.page(index)
#        if IDs == [] : break
#        for ID in IDs:
#          if ID[0] in self.data :
#            self.SET();
#            return self.data
#          else:
#            self.data.append(ID[0])
#            self.data.sort()
#            self.ADD(ID[0],ID[1])
#        print('rendered page : ',index)
#        self.SET(); index+=1
#     return self.data
#   #-------------------------------------------------------------
#   def train(self,index):
#     val=self.db.GET(index)
#     if val==[]:
#       IDs = self.page(index)
#       if IDs == [] : return False
#       self.db.SET(index,IDs)
#       return True
#     else:
#       return True


# m=Missing_ID()

# Routes
# @app.route('/recieveimage')
# # init of the whole process (can also refresh the database)
# def recieveImage():
#   res={
#     "status":"success"
#   }
#   return jsonify(res)

# @app.route('/flexsearch')
# # Returning best five matched images + captured image
# def flexSearch():
#   res={
#     "status":"success"
#   }
#   return jsonify(res)

# @app.route('/imagemapping')
# # Returning the best matched image from the five
# def imageMapping():
#   res={
#     "status":"success"
#   }
#   return jsonify(res)

@app.route('/result')
# Returning the details of the person
def result():
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
    return jsonify(res)


# @app.route('/ping')
# def ping():
#     index = request.args.get("x")
#     if m.train(int(index)):
#         return {'state': 1}
#     else:
#         return {'state': 0}


# init
if __name__ == '__main__':
    app.run(debug=True)
