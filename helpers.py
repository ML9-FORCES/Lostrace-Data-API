class Database:
  def __init__(self,database):
    self.db = database.db.Data
  #-------------------------------------------------------------
  def GET(self,ID) :
    mydoc = self.db.find({"_id":ID})
    for json in mydoc: return json['Array']
    self.db.insert_one({"_id":ID,"Array":[]})
    return []
 #-------------------------------------------------------------
  def SET(self,ID,VALUE):
    query = {"_id":ID}
    value = {"$set":{"Array":VALUE}}
    self.db.update_one(query,value)


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


class Reverse_search:
  def __init__(self):
    pass
  def vectorize(self,path):
    if 'http' in path:
      img=None
    else:
      img=None
    
