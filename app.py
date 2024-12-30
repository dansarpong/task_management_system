from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a secure random key in production
oauth = OAuth(app)

oauth.register(
    name='oidc',
    authority='https://cognito-idp.eu-west-1.amazonaws.com/eu-west-1_E7fP27kIs',
    client_id='5v50qj5qurvl71bhut7r34uor1',
    client_secret='<client secret>',
    server_metadata_url='https://cognito-idp.eu-west-1.amazonaws.com/eu-west-1_E7fP27kIs/.well-known/openid-configuration',
    client_kwargs={'scope': 'phone openid email'}
)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/login')
def login():
    # Alternate option to redirect to /authorize
    # redirect_uri = url_for('authorize', _external=True)
    # return oauth.oidc.authorize_redirect(redirect_uri)
    return oauth.oidc.authorize_redirect('https://d84l1y8p4kdic.cloudfront.net')

@app.route('/authorize')
def authorize():
    token = oauth.oidc.authorize_access_token()
    user = token['userinfo']
    session['user'] = user
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
