# Flex Algo Implementation 2022 Smart India Hackathon
# Contributors Garvit Chouhan, Kaustub Dutt Pandey, Chelsi Jain


#Dependencies
import threading


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

