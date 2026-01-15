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
