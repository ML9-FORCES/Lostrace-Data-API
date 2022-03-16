import face_recognition
import tempfile
import urllib.request
import numpy as np
from sklearn.neighbors import NearestNeighbors
import requests
from bs4 import BeautifulSoup
import threading

#############################################################################################################################

class ThreadWithResult(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)
        
#############################################################################################################################

class expresso:
  def __init__(self):
    self.batch_size=25
  #---------------------------------------------------------
  def batch(self,Process,input_list):
    packet =[ ThreadWithResult(target = Process,args=(i,)) for i in input_list]
    for instance in packet: instance.start()
    for instance in packet: instance.join()  
    res = [ instance.result for instance in packet]
    return res
  #---------------------------------------------------------
  def brew(self,Process,Input_list):
    res=[]
    for i in range(0,len(Input_list),self.batch_size):
      res=res+self.batch(Process,Input_list[i:i+self.batch_size])
    return res

#############################################################################################################################

class Retrive:
  def __init__(self):
    self.URL = 'https://trackthemissingchild.gov.in/trackchild/photograph_missing.php?page='
    self.url = 'https://ml9-forces.github.io/Lostrace-Database/'
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
  def fetch_dummy(self):
    x = requests.get(self.url)
    soup = BeautifulSoup(x.text,'html.parser')
    img_tag = soup.findAll('img',alt_='')
    names = []
    for alt_tag in img_tag:
      names.append(alt_tag['alt'])
    return names
  #-------------------------------------------------------------
  def fetch_real(self):
    data=expresso().brew(self.page,[i for i in range(1,11)])
    missing_ids=[]
    for i in data:
       for j in i:
         missing_ids.append(j)
    return missing_ids
  #-------------------------------------------------------------
  def get(self,data,state):
    if state:
      return [i for i in self.fetch_dummy() if i not in data]
    else:
      alpha=self.fetch_real()
      try: key=alpha.index(data[0]); return alpha[:key]
      except: return []

#############################################################################################################################

class Flex_Search:
  def __init__(self):
    self.neighbors=10
    self.model = NearestNeighbors(n_neighbors=self.neighbors, algorithm='brute', metric='euclidean')
  #-------------------------------------------------
  def vector(self,path):
    try:
      if 'http' in path:
        format = '.'+path.split('.')[-1]
        temp = tempfile.NamedTemporaryFile(suffix=format)
        urllib.request.urlretrieve(path,temp.name)
        img = face_recognition.load_image_file(temp.name)
        temp.close()
      else: img = face_recognition.load_image_file(path)
      return face_recognition.face_encodings(img)[0]
    except: return np.zeros(128)
  #-------------------------------------------------
  def find(self,path,data_arr,vector_arr):
    self.model.fit(vector_arr)
    vector = [self.vector(path)]
    distances,indices = self.model.kneighbors(vector)
    result_arr=[]; distance_arr=[]
    for i,ind in enumerate(indices[0]):
      if face_recognition.compare_faces([vector_arr[ind]], vector[0])[0]:
        result_arr.append(data_arr[ind])
        distance_arr.append(distances[0][i])
    try:
      res=[[x,y] for y,x in sorted(zip(distance_arr,result_arr))][0][0]
      res=info().fetch(res)
    except:
      res={'flag':0}
    return res

#############################################################################################################################

class Database:
  def __init__(self,database,state=False):
    self.db = database.db.Dataset
    if state: self.id = ["Dummy_Data"]
    else: self.id = [0,1,2,3,4,5,6]
    self.data=[]
    self.vector=[] 
    self.state=state
    self.inter_data=[]
    self.inter_vector=[]
  #-------------------------------------------------------------
  def get(self):
    for index in self.id:
      for json in self.db.find({"_id":index}): 
        self.data+=json['data'];self.vector+=[np.array(i) for i in json['vector']]
  #-------------------------------------------------------------
  def fetch(self):
    self.inter_data = Retrive().get(self.data,self.state)
  #-------------------------------------------------------------
  def encode(self):
    if self.inter_data==[]: return 0
    vectorize = lambda x : Flex_Search().vector(info().img(x))
    #self.inter_vector = expresso().brew(vectorize,self.inter_data)
    for i in self.inter_data:
      self.inter_vector.append(vectorize(i))
  #-------------------------------------------------------------
  def push(self):
    if self.inter_data==[]: return 0
    self.data=self.inter_data+self.data
    self.vector=self.inter_vector+self.vector
    if self.state:
      data,vector=self.data,self.vector
    else:
      for json in self.db.find({"_id":0}):
        data=self.inter_data+json['data'] 
        vector=self.inter_vector+json['vector']
    query = {"_id":self.id[0]}
    vector = [list(i) for i in vector]
    value = {"$set":{"data":data,"vector":vector}}
    self.db.update_one(query,value)
    self.inter_data,self.inter_vector=[],[]

#############################################################################################################################

class info:
  def __init__(self):
    self.img_r = lambda profile : "https://trackthemissingchild.gov.in/trackchild/intra_trackchild/images_missing/"+ profile +".jpg"
    self.profile = lambda ID : "https://trackthemissingchild.gov.in/trackchild/missing_dtl.php?missing_id=" + ID
    self.report = lambda profile : "https://trackthemissingchild.gov.in/trackchild/photograph_info_ps.php?profile_no=" +profile +"&return_page=photograph_missing.php&type=missing&authority=1"
    self.img_d = lambda file_name : 'https://ml9-forces.github.io/Lostrace-Database/media/original/'+file_name 
  #-------------------------------------------------------------
  def img(self,Input):
    if type(Input)==type([]): return self.img_r(Input[1])
    else: return self.img_d(Input)
  #-------------------------------------------------------------
  def fetch(self,Input):
    if type(Input)==type([]):
      details = self.personal_details(Input)
      res={}
      res["Img"] = self.img_r(Input[1])
      res["Report_link"] = self.report(Input[1])
      res["Profile_link"] = self.profile(Input[0]) 
      res["Name"] = details[0]
      res["Current_Age"] = details[1]
      res["Gender"] = details[2]
      res["Father_Name"] = details[3]
      res["Place_of_Missing"] = details[4]
      res["Date_of_Missing"] = details[5]
      res["flag"]=1
      return res
    else:
      res={}
      res["Img"] = self.img_d(Input)
      res["Report_link"] = "https://trackthemissingchild.gov.in/trackchild/photograph_info_ps.php?profile_no=3281805mpw20220010&return_page=photograph_missing.php&type=missing&authority=1"
      res["Profile_link"] = "https://trackthemissingchild.gov.in/trackchild/missing_dtl.php?missing_id=47.46.52.45.52.44.49.105.108.115.46.44.46.46.44.44.45.44.102#verticalTab1"
      res["Name"] = Input.split('.')[0]
      res["Current_Age"] = "17 Years 0 Months 6 Days"
      res["Gender"] = "MALE"
      res["Father_Name"] = "BHUDEB RAJAK"
      res["Place_of_Missing"] = "SREEBHUMI"
      res["Date_of_Missing"] = "10/03/2022"
      res["flag"]=1
      return res
  #-------------------------------------------------------------
  def personal_details(self,array):
    url = self.profile(array[0])
    html = requests.get(url)
    scrapper = BeautifulSoup(html.text,'html.parser')
    p_tags = scrapper.findAll('p')
    details=[]
    for para in p_tags:
      details += [data.replace(u'\xa0', u'') for data in para.get_text().split(":")]
    return details[1::2]

#############################################################################################################################
