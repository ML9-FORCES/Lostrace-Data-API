# Flex Algo Implementation 2022 Smart India Hackathon
# Contributors Garvit Chouhan, Kaustub Dutt Pandey, Chelsi Jain


#Dependencies
import numpy as np


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
      return json['data'],[ np.array(i) for i in json['vector'] ]
      
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

