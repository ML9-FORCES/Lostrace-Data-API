# Flex Algo Implementation 2022 Smart India Hackathon
# Contributors Garvit Chouhan, Kaustub Dutt Pandey, Chelsi Jain


#Dependencies
from Flex_Algo.Retrive_Module import *
from Flex_Algo.Flex_Module import *
from Flex_Algo.Database_Module import *
from Flex_Algo.Info_Module import *
import tempfile


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
    self.res            = {}
    
  #-------------------------------------------------------------
 
  def _load_form_Image_( self, File_Object ):
    #...............
    Format = '.' + File_Object.filename.split('.')[-1]
    File = tempfile.NamedTemporaryFile( suffix = Format )
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
      res = self._flex_.search(self._Query_Vector_,self._Data_,self._Vector_)
      if res['Phase']: 
        result_arr.append(res['Data'])
        distance_arr.append(res['Score'])
      else:
        self.res = res;
        if res['error']=='No Face Detected': break
    try: 
      res = [[x,y] for y,x in sorted(zip(distance_arr,result_arr))][0][0]
      self.res = self._info_.fetch(res)
    except: pass


#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------   

