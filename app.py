import os
import sdk_helper
from flask import Flask, redirect, url_for, session, render_template, request

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Route for the home page
@app.route('/')
def index():
    user = session.get('user')
    if not user:
        return render_template('index.html')
    return redirect(url_for('dashboard'))

# Route for the dashboard page
@app.route('/dashboard')
def dashboard():
    user = sdk_helper.get_user_details(session['user'])
    roles = sdk_helper.get_user_groups(user['Username'])
    return render_template('dashboard.html', role=roles[0]['GroupName'])

# Route for the login page and handling login logic
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = sdk_helper.log_in_user(username, password)
        session['user'] = response['AuthenticationResult']['AccessToken']
        return redirect(url_for('dashboard'))

    return render_template('login.html')

# Route for the signup page
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        group_name = request.form['group_name']
        try:
            response = sdk_helper.sign_up_user(username, password, email, group_name)
        except Exception as e:
            return str(e)
        session['username'] = username
        return redirect(url_for('confirm'))

    return render_template('signup.html')

# Route for the confirmation page
@app.route('/confirm', methods=['POST', 'GET'])
def confirm():
    if request.method == 'POST':
        print(request.form)
        confirmation_code = request.form['code']
        response = sdk_helper.confirm_user(session['username'], confirmation_code)
        session.pop('username', None)
        print(response)
        return redirect(url_for('login'))

    return render_template('confirm.html')

# Route for logging out the user
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
