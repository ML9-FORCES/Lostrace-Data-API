# Flex Algo Implementation 2022 Smart India Hackathon
# Contributors Garvit Chouhan, Kaustub Dutt Pandey, Chelsi Jain

#Dependencies
from sklearn.neighbors import NearestNeighbors
from bs4 import BeautifulSoup
import face_recognition
import urllib.request
import numpy as np
import threading
import tempfile
import requests


#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------


class ThreadWithResult(threading.Thread):

  """ 
  Muti-Threading Utility For Function Return Object 
  ...
  """
  
  #---------------------------------------------------------
  
  def __init__( self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None ):
    #...............
    def function():
      self.result = target(*args, **kwargs)
    super().__init__(group=group, target=function, name=name, daemon=daemon)

   
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------


class Expresso:

  """ 
  Expresso helps in Multi-Threading Process for Fast Computation 
  ...
  
  Initialize
  ----------
  Expresso(batch_size)
      Initialize batch_size Workers

  Methods
  -------
  brew(Process,Input_list)
      Returns Output List Compiled With batch_size Workers
  ...
  """
  
  #---------------------------------------------------------
  
  def __init__( self, batch_size ):
    #...............
    self._batch_size_=batch_size
    
  #---------------------------------------------------------
  
  def _batch_( self, Process, Input_list ):
    #...............
    packet = [ ThreadWithResult(target = Process,args=(i,)) for i in Input_list ]
    for instance in packet: instance.start()
    for instance in packet: instance.join()  
    Output_list = [ instance.result for instance in packet]
    return Output_list
    
  #---------------------------------------------------------
  
  def brew( self, Process, Input_list ):
    #...............
    Output_list = []
    for i in range(0,len(Input_list),self._batch_size_):
      Output_list = Output_list + self._batch_( Process, Input_list[i:i+self._batch_size_] )
    return Output_list


#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------


class Retrive:

  """ 
  Retrives The New Data Points In Realtime Dataset
  ...
  
  Initialize
  ----------
  Retrive(Database_Object)
      Initialize Retrive Object

  Methods
  -------
  get(Mode)
      Mode : True  -> Dummy-Dataset
             False -> Real-Dataset
      Returns : New Data-Points List
  ...
  """

  #------------------------------------------------------------

  def __init__( self, Database_Object ):
    #...............
    self.Database = Database_Object
    self.URL_R = 'https://trackthemissingchild.gov.in/trackchild/photograph_missing.php?pagination=pagination&filter=child&page='
    self.URL_D = 'https://ml9-forces.github.io/Lostrace-Database/'
    
  #-------------------------------------------------------------

  def _extract_( self, page_number ):
    #...............
    web = requests.post(self.URL_R+str(page_number))
    soup = BeautifulSoup(web.text,'html.parser')
    achors = soup.findAll('a',class_='thumbnail')
    missing_ids = []
    for block in achors:
      if block["data-categories"][:5] == "child":
        value=block['value']
        id_index = value.find("missing_id=")+11
        Profile_no_index = value.find("profile_no=")+11
        ID = value[id_index:id_index+60]
        Profile_no = value[Profile_no_index:Profile_no_index+18]
        missing_ids.append([ID,Profile_no])
    return missing_ids
    
  #-------------------------------------------------------------
  
  def _fetch_dummy_( self ):
    #...............
    web = requests.get(self.URL_D)
    soup = BeautifulSoup(web.text,'html.parser')
    img_tag = soup.findAll('img',alt_='')
    names = []
    for alt_tag in img_tag: names.append(alt_tag['alt'])
    return names
    
  #-------------------------------------------------------------
  
  def _fetch_real_( self , render_size ):
    #...............
    workers = 25 if render_size > 25 else render_size
    data = Expresso( workers ).brew( self._extract_, [ page_number for page_number in range(1,render_size+1) ] )
    missing_ids = []
    for i in data:
       for j in i: missing_ids.append(j)
    return missing_ids
    
  #-------------------------------------------------------------
  
  def get(self,Mode):
    #...............
    id_arr = ["Dummy_Data"] if Mode else [0,1]
    Existing_Data_Points=[]
    for _id in id_arr : Existing_Data_Points += self.Database.Data_Points(_id)
    if Mode:
      return [ Point for Point in self._fetch_dummy_() if Point not in Existing_Data_Points ]
    else:
      Existing_Data_Points= [ Point[1] for Point in Existing_Data_Points]
      Fetched_Data_Points=self._fetch_real_(10)
      New_Data_Points=[]
      for Point in Fetched_Data_Points:
        if Point[1] not in Existing_Data_Points: New_Data_Points.append(Point)
      return New_Data_Points
      

#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------


class Flex:
  
  """ 
  Flex Class Handles Image Encoding & Flex Search Algo
  ...
  
  Initialize
  ----------
  Flex()
      Initialize Flex Object

  Methods
  -------
  encode(Path)
      Path : Image Path or Link
      Returns : Encoded Image Vector
      
  batch_encode(Data_Points)
      Returns : Encoded Vector Array of Data_Points Respective Images
  
  search(Query_vector, data_arr, vector_arr)
      Return [Data_Point,Score] for Minimum Score of Query_vector in vector_arr
  ...
  """
  
  def __init__(self):
    #...............
    self._neighbors_=10
    self._model_ = NearestNeighbors(n_neighbors=self._neighbors_, algorithm='brute', metric='euclidean')
    self._img_r_ = lambda profile : "https://trackthemissingchild.gov.in/trackchild/intra_trackchild/images_missing/"+ profile +".jpg"
    self._img_d_ = lambda file_name : 'https://ml9-forces.github.io/Lostrace-Database/media/original/'+file_name 
  
  #-------------------------------------------------
  
  def _img_link_(self,Input):
    #...............
    if type(Input)==type([]): return self._img_r_(Input[1])
    else: return self._img_d_(Input)
  
  #-------------------------------------------------
  
  def encode(self,path):
    #...............
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
  
  def batch_encode( self, Data_Points ):
    #...............
    if Data_Points==[]: return []
    Data_Points = [self._img_link_(Point) for Point in Data_Points]
    return Expresso(5).brew( self.encode, Data_Points )
  
  #-------------------------------------------------
  
  def search( self, Query_vector, data_arr, vector_arr ):
    #...............
    self._model_.fit(vector_arr)
    vector = [Query_vector]
    if list(vector[0])==list(np.zeros(128)) : return []
    distances,indices = self._model_.kneighbors(vector)
    result_arr=[]; distance_arr=[]
    for i,ind in enumerate(indices[0]):
      if face_recognition.compare_faces([vector_arr[ind]], vector[0])[0]:
        result_arr.append(data_arr[ind])
        distance_arr.append(distances[0][i])
    try:
      res=[[x,y] for y,x in sorted(zip(distance_arr,result_arr))][0]
    except: return []
    return res


#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------


class Database:

  """ 
  Database Class Handles Data Point's & Vector's Global State
  ...
  
  Initialize
  ----------
  Database(mongo,Mode)
      Initialize Database Object
      mongo : Flask mongo-db Object
      Mode : True  -> Dummy-Dataset
             False -> Real-Dataset 

  Methods
  -------
  Data_Points(Index)
      Index : Dataset Index
      Returns : Data-Points in Dataset
      
  Get(Index)
      Index : Dataset Index
      Returns : Data-Points,Vectors in Dataset
  
  Post(New_Points,New_Vectors)
      Appends new Data_Points, vectors in Database
      Return True  -> Successfull Append
             False -> Faliure
  ...
  """
  
  def __init__(self,Mongo_Object,Mode):
    #...............
    self.db = Mongo_Object.db.Dataset
    if Mode: self.id = ["Dummy_Data"]
    else: self.id = [0,1,2,3,4,5,6]
    
  #-------------------------------------------------------------
  
  def Data_Points(self,index):
    #...............
    for json in self.db.find({"_id":index}):
      return json['data']
      
  #-------------------------------------------------------------
  
  def Get(self, index):
    #...............
    for json in self.db.find({"_id":index}):
      return json['data'],[np.array(i) for i in json['vector']]
      
  #-------------------------------------------------------------
  
  def Post(self,New_Points,New_Vectors):
    #...............
    if New_Points==[]: return True
    index=self.id[0]
    Data,Vector=self.Get(index)
    Data   = New_Points  + Data
    Vector = New_Vectors + Vector
    query = {"_id":index}
    Vector = [list(i) for i in Vector]
    value = {"$set":{"data":Data,"vector":Vector}}
    try:
      self.db.update_one(query,value)
      del Data,Vector
    except: return False
    return True

#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------

class Info:

  """ 
  Info Class extracts & formats information from data-points
  ...
  
  Initialize
  ----------
  Info()
      Initialize Info Object 

  Methods
  -------
  fetch(Data_Point)
      Returns Details in Dictionary Format
      format : {
                 Img (image_link)
                 Report_link ( Redirects to Report Page )
                 Profile_link ( Redirects to Full Profile Page )
                 Name
                 Current_Age
                 Gender
                 Father_Name
                 Place_of_Missing
                 Date_of_Missing
                 flag 
               }
      
  ...
  """
  
  def __init__(self):
    #...............
    self.img_r = lambda profile : "https://trackthemissingchild.gov.in/trackchild/intra_trackchild/images_missing/"+ profile +".jpg"
    self.profile = lambda ID : "https://trackthemissingchild.gov.in/trackchild/missing_dtl.php?missing_id=" + ID
    self.report = lambda profile : "https://trackthemissingchild.gov.in/trackchild/photograph_info_ps.php?profile_no=" +profile +"&return_page=photograph_missing.php&type=missing&authority=1"
    self.img_d = lambda file_name : 'https://ml9-forces.github.io/Lostrace-Database/media/original/'+file_name 
    
  #-------------------------------------------------------------
  
  def _Scrap_details_(self,array):
    #...............
    url = self.profile(array[0])
    html = requests.get(url)
    scrapper = BeautifulSoup(html.text,'html.parser')
    p_tags = scrapper.findAll('p')
    details=[]
    for para in p_tags:
      details += [ data.replace(u'\xa0', u'') for data in para.get_text().split(":") ]
    return details[1::2]
  
  #-------------------------------------------------------------
  
  def fetch(self,Input):
    #...............
    res={}
    if type(Input)==type([]):
      details = self._Scrap_details_(Input)
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


#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------


class Flex_Wrapper:

  """
  Flex_Wrapper Class for Combining Flex Algo Classes
  ...
  
  Dependency Class
  ----------------
  
  Retrive(Database_Object)
      - get(Mode)
  Flex()
      - encode(Path)
      - batch_encode(Data_Points)
      - search(Query_vector, data_arr, vector_arr)
  Database(mongo,Mode)
      - Data_Points(Index)
      - Get(Index)
      - Post(New_Points,New_Vectors)
  Info()
      - fetch(Data_Point)
  
  Initialize
  ---------
  Flex_Wrapper( File_Object , Mongo_Object , Mode)
      - File_Object  : Form Image 
      - Mongo_Object : Flask mongo-db Object
      - Mode : True  -> Dummy-Dataset
               False -> Real-Dataset
  
  Usage
  -----
  1. object.fetch()   >>> Fetch new data
  2. object.encode()  >>> Encode new data
  3. object.update()  >>> Updates new data & vectors over database
  4. object.search()  >>> Search Image in Dataset
  5. object.res       >>> return Final Response
  ...
  """
  
  def __init__( self, File_Object , Mongo_Object , Mode ):
    #...............
    self._flex_         = Flex()
    self._db_           = Database(Mongo_Object, Mode)
    self._retrive_      = Retrive(self._db_)
    self._info_         = Info()
    self._Query_Vector_ = self._load_form_Image_(File_Object)
    self._Mode_         = Mode
    self._Data_         = []
    self._Vector_       = []
    self.res            = { 'flag' : 0 }
    
  #-------------------------------------------------------------
 
  def _load_form_Image_( self, File_Object ):
    #...............
    Format = '.' + File_Object.filename.split('.')[-1]
    File = tempfile.NamedTemporaryFile( suffix=Format )
    File_Object.save(File.name)
    vector = self._flex_.encode(File.name)
    File.close()
    return vector
  
  #-------------------------------------------------------------
  
  def fetch( self ):
    #...............
    self._Data_ = self._retrive_.get(self._Mode_)
  
  #-------------------------------------------------------------
  
  def encode( self ):
    #...............
    self._Vector_ = self._flex_.batch_encode(self._Data_)
  
  #-------------------------------------------------------------
  
  def update( self ):
    #...............
    while True:
      if self._db_.Post(self._Data_,self._Vector_): break
  
  #-------------------------------------------------------------
  
  def search( self ):
    #...............
    result_arr=[]
    distance_arr=[]
    for index in self._db_.id:
      self._Data_,self._Vector_=self._db_.Get(index)
      value = self._flex_.search(self._Query_Vector_,self._Data_,self._Vector_)
      if bool(value): result_arr.append(value[0]); distance_arr.append(value[1])
    try: 
      res = [[x,y] for y,x in sorted(zip(distance_arr,result_arr))][0][0]
      self.res = self._info_.fetch(res)
    except: pass


#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------   
