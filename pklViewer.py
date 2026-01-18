import pickle
class User:
    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email
        self.messages = ""
        

with open("users.pkl","rb") as f:
  Users = pickle.load(f)

for i in Users:
   print(f"{i.username}\n{i.password}\n{i.email}\n{i.messages}-------------------------------\n")
print("\n \n \n \n ")

#from ollama import ChatResponse,chat
## smollm2:135m
#
#response: ChatResponse = chat(model='smollm2:135m', messages=[
#  {
#    'role': 'user',
#    'content': 'Hello',
#  },
#])
#print(response['message']['content'])
## or access fields directly from the response object
#print(response.message.content)