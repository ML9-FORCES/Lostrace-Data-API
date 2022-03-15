import face_recognition
import tempfile
import urllib.request
import numpy as np
from sklearn.neighbors import NearestNeighbors
import requests
from bs4 import BeautifulSoup
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

class Database:
  def __init__(self,database,state=False):
    if state: self.db = database.db.Dummy_Data; self.id='Dummy_Data'
    else: self.db = database.db.Real_Data; self.id='Real_Data'
  #-------------------------------------------------------------
  def GET(self) :
    mydoc = self.db.find({"_id":self.id})
    for json in mydoc: 
      return json['data'],[np.array(i) for i in json['vector']]
 #-------------------------------------------------------------
  def SET_DATA(self,data):
    query = {"_id":self.id}
    value = {"$set":{"data":data}}
    self.db.update_one(query,value)
 #-------------------------------------------------------------
  def SET_VECTOR(self,vector):
    query = {"_id":self.id}
    vector = [list(i) for i in vector]
    value = {"$set":{"vector":vector}}
    self.db.update_one(query,value)

class Flex_Search:
  def __init__(self):
    self.neighbors=10
    self.model = NearestNeighbors(n_neighbors=self.neighbors, algorithm='brute', metric='euclidean')
  #-------------------------------------------------
  def vector(self,path):
    if 'http' in path:
      format = '.'+path.split('.')[-1]
      temp = tempfile.NamedTemporaryFile(suffix=format)
      urllib.request.urlretrieve(path,temp.name)
      img = face_recognition.load_image_file(temp.name)
      temp.close()
    else: img = face_recognition.load_image_file(path)
    try: return face_recognition.face_encodings(img)[0]
    except: return np.empty(128)
  #-------------------------------------------------
  def find(self,path,data_arr,vector_arr,flag=False):
    self.model.fit(vector_arr)
    vector = [self.vector(path)]
    distances,indices = self.model.kneighbors(vector)
    result_arr=[]; distance_arr=[]
    for i,ind in enumerate(indices[0]):
      if face_recognition.compare_faces([vector_arr[ind]], vector[0])[0]:
        result_arr.append(data_arr[ind])
        distance_arr.append(distances[0][i])
    res=[[x,y] for y,x in sorted(zip(distance_arr,result_arr))] 
    if len(res)<3: res=res+[[]]*(3-len(res))
    res={'res1':res[0],'res2':res[1],'res3':res[2]}
    if flag: 
      self.plot(path)
      for i in res: self.plot(res[i][0])
    return res
  #-------------------------------------------------
  def plot(self,path):
    if 'http' in path:
      format = '.'+path.split('.')[-1]
      temp = tempfile.NamedTemporaryFile(suffix=format)
      urllib.request.urlretrieve(path,temp.name)
      plt.imshow(mpimg.imread(temp.name))
      plt.show()
      temp.close()
    else: plt.imshow(mpimg.imread(path)); plt.show()

class Missing_ID:
  def __init__(self,db):
    self.db = db
    self.URL = 'https://trackthemissingchild.gov.in/trackchild/photograph_missing.php?page='
    self.data = self.db.GET('data')
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
      Profile_no_index = value.find("profile_no=")+11
      age = int((value[age_index:age_index+3].split())[0])
      ID = value[id_index:id_index+60]
      Profile_no = value[Profile_no_index:Profile_no_index+18]
      if age<18:
        missing_ids.append([ID,Profile_no])
    return missing_ids
  #-------------------------------------------------------------
  def fetch(self,index=1):
    while True:
       IDs = self.page(index)
       if IDs == [] : break
       for ID in IDs:
         if ID[0] in self.data : 
           self.SET(); 
           return self.data
         else: 
           self.data.append(ID[0]) 
           self.data.sort()
           self.ADD(ID[0],ID[1])
       print('rendered page : ',index)
       self.SET(); index+=1
    return self.data
  #-------------------------------------------------------------
  def train(self,index):
    val=self.db.GET(index)
    if val==[]:
      IDs = self.page(index)
      if IDs == [] : return False
      self.db.SET(index,IDs)
      return True
    else:
      return True





    
