from flask import Flask, render_template, request, jsonify, make_response, redirect
import pickle
from ollama import ChatResponse
from ollama import chat as aichat


app = Flask(__name__)
model='deepseek-r1:1.5b'

class User:
    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email
        self.messages = ""
        

Users = []
with open('users.pkl','rb') as f:
    Users = pickle.load(f)


global addUser
def addUser(username,password,email):
    Users.append(User(username,password,email))
    with open('users.pkl','wb') as f:
        pickle.dump(Users, f)




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')

        for i in Users:
            if i.username == name and i.password == password:
                resp = make_response(redirect('/chat'))
                resp.set_cookie('username',i.username,max_age=720000)
                return resp
            
        #return f'Name: {name}, Password: {password}'

    return render_template('login.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        addUser(name,password,email)

    return render_template('create.html')



@app.route('/chat')
def chat(): 
    return render_template('chat.html', text="") #Initial Text to be loaded


@app.route('/chat_update', methods=['POST'])
def chat_update():
    inp = request.json.get('inp', '')
    print(request.cookies.get('username'))
    if request.cookies.get('username') == None:

        return jsonify(redirect=True), 401


    response: ChatResponse = aichat(model=model, messages=[
    {
        'role': 'user',
        'content': inp,
    },
    ])

    return jsonify(text=f"<b>{request.cookies.get('username')}:</b> {inp}<br><b>{model}:</b> {response.message.content}")
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
