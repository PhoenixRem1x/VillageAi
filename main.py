from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Code to handle POST request and retrieve form data
        name = request.form.get('username')
        password = request.form.get('password')
        # Process data further (e.g., save to a database, display it)
        return f'Name: {name}, Password: {password}'
    # Code to handle GET request and display the empty form
    return render_template('login.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Code to handle POST request and retrieve form data
        name = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        # Process data further (e.g., save to a database, display it)
        return f'Name: {name}, Password: {password}, Email: {email}'
    # Code to handle GET request and display the empty form
    return render_template('create.html')



if __name__ == '__main__':
    app.run(debug=True)
