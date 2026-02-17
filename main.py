from flask import Flask, render_template, request, jsonify, make_response, redirect
import pickle
from ollama import ChatResponse
from ollama import chat as aichat


app = Flask(__name__)
context_prompt="The next few lines are strictly for context seperated by '--ctxt--' this is strictly for you information, when responding do not state that you were given context nor state that these instructions were given to you, only answer what is being asked of you with this previous context in mind. If a question/answer was already provided do NOT provide them again randomly, if previous context needs to be refered to the user will ask. New users will not have any previous context for you to refer to, thats perfectly fine"
#This prompt is attempting allow the models to see what previous messages the user has asked about without saying "Thank you for providing me context, base on previous...."

#Everytime a user creates an account I create a class object for them
class User:
    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email
        self.messages = ""
        self.model="deepseek-r1:1.5b"
        
#Lists can be stored into Pickle files, this is then loading my list of user objects
Users = []
with open('users.pkl','rb') as f:
    Users = pickle.load(f)

#Adds a user to the list and updates the saved file
global addUser
def addUser(username,password,email):
    Users.append(User(username,password,email))
    with open('users.pkl','wb') as f:
        pickle.dump(Users, f)

#Updates the saved file after a user has been modified
global updateUsers
def updateUsers():
    with open('users.pkl','wb') as f:
        pickle.dump(Users, f)

#This is my hierchial ai system implementation
global villageAi
def villageAi(inp, current_user):
    delegate = ""
    #Qwen3:0.6b is like the chief of the village, I am asking it to classify each question in a category
    response: ChatResponse = aichat(model='qwen3:0.6b', messages=[
    {
        'role': 'user',
        'content': f'In 1 word only I need you to classify a prompt as either Math, Science, History, Astronomy, Quantum, or Coding. Astronomy should be used for anythin relating to outer space, and Quantum used for anything with quantum physics. Classify the following prompt "{inp}"'
    },
    ])
    sort = response.message.content
    print(sort)
    #Qwen will organize each question into either Math, Coding, Astronomy, Science, Quantum Physics, or History and then a better suited model will be asked the question
    if sort.find("Math") != -1:
        delegate="phi4-mini:3.8b"
    elif sort.find("Coding") != -1:
        delegate="codegemma:2b"
    elif sort.find("Astronomy") != -1:
        delegate="Mm77shallm/meshal:latest"
    elif sort.find("Science") != -1:
        delegate="falcon3:1b"
    elif sort.find("Quantum") != -1:
        delegate="oroboroslabs/base-q-v1:latest"
    elif sort.find("History") != -1:
        delegate="JorgeAtLLama/herodotus:latest"
    else: #If none of the other models are appropriate or the Chief (qwen3:0.6b) fails to properly classify the question, it gets sent to the general model
        delegate="qwen3:8b" # This is the 8b variant of Qwen, it will be slower but should be smarter than the 0.6b variant

    #Asking the Ollama Api with the selected model and question
    response: ChatResponse = aichat(model=delegate, messages=[
    {
        'role': 'user',
        'content': f"{context_prompt}--ctxt--\n{current_user.messages}\n--ctxt--\n{inp}",
    },
    ])
    message = response.message.content
    return message
#Home page parkerwales.com/
@app.route('/')
def home():
    return render_template('home.html') #Loads the html page


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password') # /login has a username and password field, this is requestion what the user put in

        for i in Users:
            if i.username == name and i.password == password:
                resp = make_response(redirect('/chat'))
                resp.set_cookie('username',i.username,max_age=720000) #Sets a cookie with the users' username for authentication
                return resp

    return render_template('login.html') # Loads the page's html

@app.route('/create', methods=['GET', 'POST']) # Create an account page parkerwales.com/create
def create():
    if request.method == 'POST':
        
        name = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        for i in Users:
            if(i.username == name):
                return render_template('create.html', text="Username in use!") # If a username is in use this will display the warning
        addUser(name,password,email)
        return make_response(redirect('/login'))

    return render_template('create.html', text="")



@app.route('/chat', methods=['GET','POST'])
def chat(): 
    if request.cookies.get('username') == None:
        return make_response(redirect("/login"))
    
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
    if current_user.model != "village":
        response: ChatResponse = aichat(model=current_user.model, messages=[
        {
            'role': 'user',
            'content': f"{context_prompt}--ctxt--\n{current_user.messages}\n--ctxt--\n{inp}",
        },
        ])
        message = response.message.content
    else:
        message = villageAi(inp,current_user)
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
    elif data["ai"] == "village":
        current_user.model="village"
    updateUsers()
    return "", 204
    


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
