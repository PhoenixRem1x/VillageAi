from flask import Flask, render_template, request, jsonify
import pickle, ollama

text = "asdasdasdasdasdadadasd"

app = Flask(__name__)

class User:
    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email

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
                return "sucess"
        return f'Name: {name}, Password: {password}'
    

    # Code to handle GET request and display the empty form
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
    return render_template('chat.html', text=text)


@app.route('/chat_update', methods=['POST'])
def chat_update():
    inp = request.json.get('inp', '')
    # later you can call ollama here
    return jsonify(text=f"{text}{inp}")




if __name__ == '__main__':
    app.run(debug=True)
