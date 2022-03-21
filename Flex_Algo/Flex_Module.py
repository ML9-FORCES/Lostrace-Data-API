# Flex Algo Implementation 2022 Smart India Hackathon
# Contributors Garvit Chouhan, Kaustub Dutt Pandey, Chelsi Jain


#Dependencies
from sklearn.neighbors import NearestNeighbors
import face_recognition
import urllib.request
import numpy as np
import tempfile


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
      Return { 'Phase':True, 'Data':<data-point>, 'Score':<min-distance> }
             { 'Phase':False, 'error':<error-msg> }
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
    Data_Points = [ self._img_link_(Point) for Point in Data_Points ]
    return [ self.encode(Point) for Point in Data_Points ]
  
  #-------------------------------------------------
  
  def search( self, Query_vector, data_arr, vector_arr ):
    #...............
    self._model_.fit(vector_arr)
    vector = [Query_vector]
    if list(vector[0]) == list(np.zeros(128)): return { 'Phase':False, 'error':'No Face Detected' }
    distances,indices = self._model_.kneighbors(vector)
    result_arr=[]; distance_arr=[]
    for i,ind in enumerate(indices[0]):
      if face_recognition.compare_faces([vector_arr[ind]], vector[0])[0]:
        result_arr.append(data_arr[ind])
        distance_arr.append(distances[0][i])
    try:
      res=[[x,y] for y,x in sorted(zip(distance_arr,result_arr))][0]
    except: return { 'Phase':False, 'error':'Person Not Found' }
    return { 'Phase':True, 'Data':res[0], 'Score':res[1] }


#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------

