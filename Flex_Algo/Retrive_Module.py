# Flex Algo Implementation 2022 Smart India Hackathon
# Contributors Garvit Chouhan, Kaustub Dutt Pandey, Chelsi Jain

#Dependencies
from Flex_Algo.Expresso_Module import *
from bs4 import BeautifulSoup
import requests


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
    self._Database_ = Database_Object
    self._URL_R_ = 'https://trackthemissingchild.gov.in/trackchild/photograph_missing.php?pagination=pagination&filter=child&page='
    self._URL_D_ = 'https://ml9-forces.github.io/Lostrace-Database/'
    
  #-------------------------------------------------------------

  def _extract_( self, page_number ):
    #...............
    web = requests.post(self._URL_R_+str(page_number))
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
    web = requests.get(self._URL_D_)
    soup = BeautifulSoup(web.text,'html.parser')
    img_tag = soup.findAll('img',alt_='')
    names = []
    for alt_tag in img_tag: names.append(alt_tag['alt'])
    return names
    
  #-------------------------------------------------------------
  
  def _fetch_real_( self , render_size ):
    #...............
    workers = 25 if render_size > 25 else render_size*2
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
    for _id in id_arr : Existing_Data_Points += self._Database_.Data_Points(_id)
    if Mode:
      return [ Point for Point in self._fetch_dummy_() if Point not in Existing_Data_Points ]
    else:
      Existing_Data_Points= [ Point[1] for Point in Existing_Data_Points ]
      Fetched_Data_Points=self._fetch_real_(10)
      New_Data_Points=[]
      for Point in Fetched_Data_Points:
        if Point[1] not in Existing_Data_Points: New_Data_Points.append(Point)
      return New_Data_Points
      

#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------

