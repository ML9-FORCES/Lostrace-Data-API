# Flex Algo Implementation 2022 Smart India Hackathon
# Contributors Garvit Chouhan, Kaustub Dutt Pandey, Chelsi Jain


#Dependencies
from bs4 import BeautifulSoup
import requests


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
               }
  ...
  """
  
  def __init__(self):
    #...............
    self._img_r_ = lambda profile : "https://trackthemissingchild.gov.in/trackchild/intra_trackchild/images_missing/"+ profile +".jpg"
    self._profile_ = lambda ID : "https://trackthemissingchild.gov.in/trackchild/missing_dtl.php?missing_id=" + ID
    self._report_ = lambda profile : "https://trackthemissingchild.gov.in/trackchild/photograph_info_ps.php?profile_no=" +profile +"&return_page=photograph_missing.php&type=missing&authority=1"
    self._img_d_ = lambda file_name : 'https://ml9-forces.github.io/Lostrace-Database/media/original/'+file_name 
    
  #-------------------------------------------------------------
  
  def _Scrap_details_(self,array):
    #...............
    url = self._profile_(array[0])
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
      res["Img"] = self._img_r_(Input[1])
      res["Report_link"] = self._report_(Input[1])
      res["Profile_link"] = self._profile_(Input[0]) 
      res["Name"] = details[0]
      res["Current_Age"] = details[1]
      res["Gender"] = details[2]
      res["Father_Name"] = details[3]
      res["Place_of_Missing"] = details[4]
      res["Date_of_Missing"] = details[5]
      return res
    else:
      res["Img"] = self._img_d_(Input)
      res["Report_link"] = "https://trackthemissingchild.gov.in/trackchild/photograph_info_ps.php?profile_no=3281805mpw20220010&return_page=photograph_missing.php&type=missing&authority=1"
      res["Profile_link"] = "https://trackthemissingchild.gov.in/trackchild/missing_dtl.php?missing_id=47.46.52.45.52.44.49.105.108.115.46.44.46.46.44.44.45.44.102#verticalTab1"
      res["Name"] = Input.split('.')[0]
      res["Current_Age"] = "17 Years 0 Months 6 Days"
      res["Gender"] = "MALE"
      res["Father_Name"] = "BHUDEB RAJAK"
      res["Place_of_Missing"] = "SREEBHUMI"
      res["Date_of_Missing"] = "10/03/2022"
      return res


#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------

