import pickle
class User:
    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email

asd = []
asd.append(User("test","pass","@eample.com"))
print(asd)
print(asd[0].email)

with open('mylist.pkl', 'wb') as f:
    pickle.dump(asd, f)

with open('mylist.pkl','rb') as f:
    list2 = pickle.load(f)
print("------"+list2[0].email)


print("\n \n \n \n ")
from ollama import ChatResponse,chat
# smollm2:135m

response: ChatResponse = chat(model='smollm2:135m', messages=[
  {
    'role': 'user',
    'content': 'Hello',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)