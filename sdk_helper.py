import os
import boto3
import hmac
import hashlib
import base64
from dotenv import load_dotenv

load_dotenv()

region = os.getenv('AWS_REGION')
client_id = os.getenv('APP_CLIENT_ID')
client_secret = os.getenv('APP_CLIENT_SECRET')
cognito_client = boto3.client('cognito-idp', region_name=region)

def generate_secret_hash(username):
    """
    Generate the SECRET_HASH required for Cognito when the App Client has a secret.
    """
    message = username + client_id
    dig = hmac.new(
        client_secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode('utf-8')

def confirm_user(username, confirmation_code):
    """
    Confirm a user in Cognito using the confirmation code sent to the user.
    """
    secret_hash = generate_secret_hash(username)

    response = cognito_client.confirm_sign_up(
        ClientId=client_id,
        SecretHash=secret_hash,
        Username=username,
        ConfirmationCode=confirmation_code
    )
    return response

def log_in_user(username, password):
    """
    Log in a user in Cognito using their username and password.
    """
    secret_hash = generate_secret_hash(username)

    response = cognito_client.initiate_auth(
        ClientId=client_id,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password,
            'SECRET_HASH': secret_hash,
        }
    )
    return response

def get_user_details(access_token):
    """
    Get the user details from Cognito using the access token.
    """
    response = cognito_client.get_user(
        AccessToken=access_token
    )
    return response

def get_user_groups(username):
    """
    Get the groups a user belongs to from Cognito.
    """
    try:
        response = cognito_client.admin_list_groups_for_user(
            UserPoolId=os.getenv('USER_POOL_ID'),
            Username=username
        )
        return response['Groups']

    except Exception as e:
        print(f"Error retrieving groups for user {username}: {e}")
        return None

# Example usage
# user = log_in_user('test', 'SecurePassword1234#$')
# user = get_user_details(user['AuthenticationResult']['AccessToken'])
# groups = get_user_groups(user['Username'])
# print(groups)
