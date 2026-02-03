from flask import Flask, render_template, request, jsonify, make_response, redirect
import pickle
from ollama import ChatResponse
from ollama import chat as aichat


app = Flask(__name__)
model='smollm2:135m'
context_prompt="The next few lines are strictly for context seperated by '--ctxt--' this is strictly for you information, when responding do not state that you were given context nor state that these instructions were given to you, only answer what is being asked of you with this previous context in mind. If a question/answer was already provided do NOT provide them again randomly, if previous context needs to be refered to the user will ask. New users will not have any previous context for you to refer to, thats perfectly fine"

class User:
    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email
        self.messages = ""
        self.model="deepseek-r1:1.5b"
        

Users = []
with open('users.pkl','rb') as f:
    Users = pickle.load(f)


global addUser
def addUser(username,password,email):
    Users.append(User(username,password,email))
    with open('users.pkl','wb') as f:
        pickle.dump(Users, f)

global updateUsers
def updateUsers():
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
        for i in Users:
            if(i.username == name):
                return render_template('create.html', text="Username in use!")
        addUser(name,password,email)
        return make_response(redirect('/login'))

    return render_template('create.html', text="")



@app.route('/chat', methods=['GET','POST'])
def chat(): 
    for i in Users:
        if i.username == request.cookies.get('username'):
            return render_template('chat.html', text=i.messages) #Initial Text to be loaded
        
    if request.method == 'POST':
        print(request.form.get('ai'))
    


@app.route('/chat_update', methods=['POST'])
def chat_update():
    inp = request.json.get('inp', '')
    print(request.cookies.get('username'))
    if request.cookies.get('username') == None:
        return jsonify(redirect=True), 401
    for i in Users:
        if i.username == request.cookies.get('username'):
            current_user = i

    response: ChatResponse = aichat(model=current_user.model, messages=[
    {
        'role': 'user',
        'content': f"{context_prompt}--ctxt--\n{current_user.messages}\n--ctxt--\n{inp}",
    },
    ])
    message = response.message.content
    # Ai models like to output in markdown, Im not using mardown so the next bit is going to be a python interpretation of markdown using to switch between opening and closing elements
    print(message)
    for c in range(message.count("**")):
        message = message.replace("**","<i>",1)
        message = message.replace("**","</i>",1)
    if (message.count("<i>") > message.count("</i>")):
        message += "</i>"
    print(message)

    current_user.messages+=f"<b>{request.cookies.get('username')}:</b> {inp}<br><b>{current_user.model}:</b> {message}<br>"

    updateUsers()

    
    return jsonify(text=current_user.messages)

@app.route('/chat_clear', methods=['POST'])
def chat_clear():
    print(request.cookies.get('username'))
    if request.cookies.get('username') == None:
        return jsonify(redirect=True), 401
    for i in Users:
        if i.username == request.cookies.get('username'):
            current_user = i
    print("Clearing Messages")
    current_user.messages = " "
    updateUsers()

@app.route("/select_ai", methods=["POST"])
def select_ai():
    if request.cookies.get('username') == None:
        return jsonify(redirect=True), 401
    for i in Users:
            if i.username == request.cookies.get('username'):
                current_user = i
    data = request.get_json()
    print(data["ai"])
    if data["ai"] == "deepseek":
        current_user.model="deepseek-r1:1.5b"
    elif data["ai"] == "meta":
        current_user.model="llama3.2:1b"
    elif data["ai"] == "gemma":
        current_user.model="gemma3:1b"
    elif data["ai"] == "lfm2":
        current_user.model="lfm2.5-thinking:latest"
    updateUsers()
    return "", 204
    


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
