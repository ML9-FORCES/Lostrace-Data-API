# Flex Algo Implementation 2022 Smart India Hackathon
# Contributors Garvit Chouhan, Kaustub Dutt Pandey, Chelsi Jain


#Dependencies
from Flex_Algo.Flex_Wrapper_Module import *
import threading


#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------   

class Background_Task:
  
  """ 
  Background_Task Class Manages Flex Search in Background with Threaded Process
  ...
  
  Initialize
  ----------
  Background_Task(Mongo_Object)
      Initialize Background_Task Object 

  Methods
  -------
  run(File_Object,Mode)
    Initialize Flex Search
    Return : Url(GET) for Search Status Query
             { 'Task' : <Url> }
  
  state(Task_id)
    Return Search Status : { 'Phase':<_>, 'Info':<_> }
    - Phase: Success      Info : Person-Details (Dictionary)
    - Phase: Process      Info : Current Running Process (String)
    - Phase: Failure      Info : Error Message (String)
  ...
  """
  
  def __init__(self,Mongo_Object):
    #...............
    self._mongo_ = Mongo_Object
    self._task_ = Mongo_Object.db.Tasks
   
  #------------------------------------------------------------- 
    
  def _Process_( self, Affine, Task_id):
    #...............
    self._update_(Task_id,{'Phase':'Process','Info':'Fetching New Data'})
    print('Fetching New Data')
    Affine.fetch() 
    #...............
    self._update_(Task_id,{'Phase':'Process','Info':'Encoding New Data'})
    print('Encoding New Data')
    Affine.encode()
    #............... 
    self._update_(Task_id,{'Phase':'Process','Info':'Updating Database State'})
    print('Updating Database State')
    Affine.update()
    #...............
    self._update_(Task_id,{'Phase':'Process','Info':'Flex Searching Image'})
    print('Flex Searching Image')
    Affine.search()
    print('Search Done')
    #...............
    if 'error' in Affine.res :
      self._update_(Task_id,{'Phase':'Failure','Info':Affine.res['error']})
    else:
      self._update_(Task_id,{'Phase':'Success','Info':Affine.res})
  
  #-------------------------------------------------------------
  
  def _update_(self,task_id,value):
    #...............
    query = {"_id":task_id}
    value = {"$set":{"value":value}}
    self._task_.update_one(query,value)
  
  #-------------------------------------------------------------
       
  def run(self,File_Object,Mode):
    #...............
    url = lambda ID : 'https://lostrace-data-api.herokuapp.com/state/' + str(ID)
    res={ 'value':{} }
    Task_id = self._task_.insert_one(res).inserted_id
    if File_Object == None : self._update_(Task_id,{'Phase':'Failure','Info':'No Image Uploaded'})
    else:
      print('Encoding Query Image')
      Affine = Flex_Wrapper(File_Object,self._mongo_,Mode)
      task = ThreadWithResult( target = self._Process_, args=(Affine,Task_id) )
      task.start()
    return {'Task':url(Task_id)}
  
  #-------------------------------------------------------------
   
  def state(self,task_id):
    #...............
    task = self._task_.find_one_or_404(task_id)
    return task['value']
    

#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------    
