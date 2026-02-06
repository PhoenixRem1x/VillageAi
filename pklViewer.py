import pickle
class User:
    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email
        self.messages = ""
        self.model="deepseek-r1:1.5b"
        

#with open("users.pkl","wb") as f:
#   pickle.dump([User('user','pass','email')],f)


with open("users.pkl","rb") as f:
  Users = pickle.load(f)

for i in Users:
  print(f"{i.username}\n{i.password}\n{i.email}\n{i.messages}\n{i.model}-------------------------------\n")
  #i.messages=""
  i.model="smollm2:135m"
  with open('users.pkl','wb') as f:
        pickle.dump(Users, f)
  
print("\n \n \n \n ")

