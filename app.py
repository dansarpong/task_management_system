import os
import json
import requests
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, render_template, session, request

load_dotenv(override=True)

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)
url = os.getenv('API_URL')


# Route for the home page
@app.route('/')
def index():
    if session.get('username') is None:
        return render_template('index.html')
    return redirect(url_for('dashboard'))


# Route for the dashboard page
@app.route('/dashboard')
def dashboard():
    # Default view
    if 'Admins' in session['groups']:
        tasks = get_tasks(session['IdToken'])
        users = get_users(session['IdToken'])
        return render_template('admin.html', role='Admin', tasks=tasks, users=users)
    elif 'Members' in session['groups']:
        tasks = get_tasks(session['IdToken'], session['username'])
        return render_template('members.html', role='Member', tasks=tasks)

    return redirect(url_for('login'))


# Route for the login page and handling login logic
@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    Log in a user and store their session information.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        path = "/users/login"
        payload = json.dumps({
            "username": username,
            "password": password
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            url + path, headers=headers, data=payload).json()
        session['username'] = username
        session['groups'] = response['Groups']
        session['IdToken'] = response['AuthenticationResult']['IdToken']
        session['AccessToken'] = response['AuthenticationResult']['AccessToken']

        return redirect(url_for('dashboard'))

    return render_template('login.html')


# Route for logging out the user
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# Route for the signup page
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    """
    Sign up a new user and send a confirmation code to their email.
    """
    if request.method == 'POST':
        group_name = request.form['group_name'].capitalize()
        session['username'] = request.form['username']
        session['email'] = request.form['email']
        password = request.form['password']
        path = "/users/signup"
        payload = json.dumps({
            "username": session['username'],
            "email": session['email'],
            "password": password,
            "group_name": group_name
        })
        headers = {'Content-Type': 'application/json'}
        requests.post(url + path, headers=headers, data=payload)

        return redirect(url_for('confirm'))

    return render_template('signup.html')


# Route for the confirmation page
@app.route('/confirm', methods=['POST', 'GET'])
def confirm():
    """
    Confirm a user using the confirmation code sent to their email
    and redirect to the login page.
    """
    if request.method == 'POST':
        confirmation_code = request.form['code']
        try:
            path = "/users/signup/confirm"
            payload = json.dumps({
                "username": session['username'],
                "email": session['email'],
                "confirmation_code": confirmation_code
            })
            headers = {'Content-Type': 'application/json'}
            requests.post(url + path, headers=headers, data=payload)
        except Exception as e:
            return render_template('error.html', error_code=500, error_message=str(e))
        finally:
            session.pop('username', None)
        return redirect(url_for('login'))

    return render_template('confirm.html')


# Route for the settings page
@app.route('/settings', methods=['POST', 'GET'])
def settings():
    """
    Display and update user settings.
    """
    path = "/settings"
    payload = json.dumps({"accessToken": session['AccessToken']})
    headers = {'Content-Type': 'application/json'}

    if request.method == 'POST':
        headers['Token'] = session['IdToken']
        email_notifications = request.form.get('email_notifications') == 'on'
        # enable or disable email notifications
        if email_notifications and not session["email_notifications"]:
            requests.post(url + path, headers=headers, data=payload)
        elif not email_notifications and session["email_notifications"]:
            requests.delete(url + path, headers=headers, data=payload)
        return redirect(url_for('dashboard'))

    response = requests.get(url + path, data=payload, headers=headers).json()
    session["email_notifications"] = response['verified']
    return render_template('settings.html', email_notifications=session["email_notifications"])


# Tasks routes
@app.route('/create_task', methods=['POST'])
def create_task():
    """
    Create a task for the user and redirect to the dashboard.
    """
    path = "/tasks"
    task_name = request.form['name']
    task_status = request.form['status']
    task_assignee = request.form['assignee']
    task_deadline = request.form['deadline'] or None
    payload = json.dumps({
        "name": task_name,
        "status": task_status,
        "assignee": task_assignee,
        "deadline": task_deadline
    })
    headers = {
        'Content-Type': 'application/json',
        'Token': session['IdToken']
    }
    requests.post(url + path, headers=headers, data=payload)
    return redirect(url_for('dashboard'))


@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    """
    Update a task in the database and redirect to the dashboard.
    """
    path = f"/tasks/{task_id}"
    task_name = request.form['name']
    task_status = request.form['status']
    task_assignee = request.form['assignee']
    task_deadline = request.form['deadline'] or None
    payload = json.dumps({
        "name": task_name,
        "status": task_status,
        "assignee": task_assignee,
        "deadline": task_deadline
    })
    headers = {
        'Content-Type': 'application/json',
        'Token': session['IdToken']
    }
    requests.put(url + path, headers=headers, data=payload)
    return redirect(url_for('dashboard'))


# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Page not found"), 404


@app.errorhandler(Exception)
def internal_server_error(e):
    return render_template('error.html', error_code=500, error_message="Internal error: " + str(e)), 500


# Helper functions
def get_tasks(IdToken, username=None):
    """
    Get all tasks for the user.
    """
    path = "/tasks"
    headers = {
        'Token': IdToken,
        'Member': username if username else ''
    }
    response = requests.get(url + path, headers=headers).json()
    return response


def get_users(IdToken):
    """
    Get all users.
    """
    path = "/users"
    headers = {'Token': IdToken}
    response = requests.get(url + path, headers=headers).json()
    return response


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
