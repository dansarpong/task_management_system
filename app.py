import os
import sdk_helper as sdk
from flask import Flask, redirect, url_for, render_template, session, request


# Initialize the Flask app
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
@app.route('/dashboard', methods=['POST', 'GET', 'PUT'])
def dashboard():
    # Default view
    if 'Admins' in session['groups']:
        tasks = sdk.get_tasks(session['IdToken'])
        return render_template('admin.html', role='Admin', tasks=tasks)
    elif 'Members' in session['groups']:
        tasks = sdk.get_tasks(session['IdToken'], session['username'])
        return render_template('members.html', role='Member', tasks=tasks)
    print(session['groups'])
    return redirect(url_for('login')) # Or return a 403 Forbidden error (later)

# Route for the login page and handling login logic
@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    Log in a user and store their session information.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            response = sdk.log_in_user(username, password)
            session['username'] = username
            session['groups'] = sdk.get_user_groups(session['username'])
            session['IdToken'] = response['AuthenticationResult']['IdToken']
            session['AccessToken'] = response[
                'AuthenticationResult']['AccessToken']
        except Exception as e:
            return str(e)

        return redirect(url_for('dashboard'))

    return render_template('login.html')


# Route for the signup page
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    """
    Sign up a new user and send a confirmation code to their email.
    """
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        group_name = request.form['group_name']
        try:
            sdk.sign_up_user(username, email, password, group_name)
        except Exception as e:
            return str(e)
        session['username'] = username
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
            sdk.confirm_user(session['username'], confirmation_code)
        except Exception as e:
            return str(e)
        finally:
            session.pop('user', None)

        return redirect(url_for('login'))

    return render_template('confirm.html')


# Route for logging out the user
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/create_task', methods=['POST'])
def create_task():
    """
    Create a task for the user and redirect to the dashboard.
    """
    task_name = request.form['name']
    task_status = request.form['status']
    task_assignee = request.form['assignee']
    task_deadline = request.form['deadline'] or None
    try:
        sdk.create_task(session['IdToken'], task_name, task_status,
                        task_assignee, task_deadline)
    except Exception as e:
        return str(e)
    return redirect(url_for('dashboard'))

@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    """
    Update a task in the database and redirect to the dashboard.
    """
    task_name = request.form['name']
    task_status = request.form['status']
    task_assignee = request.form['assignee']
    task_deadline = request.form['deadline'] or None
    try:
        sdk.update_task(session['IdToken'], task_id, task_name, task_status, task_assignee, task_deadline)
    except Exception as e:
        return str(e)
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
