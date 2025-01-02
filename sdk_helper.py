import os
import json
import hmac
import boto3
import base64
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv(override=True)
region = os.getenv('AWS_REGION')
client_id = os.getenv('APP_CLIENT_ID')
client_secret = os.getenv('APP_CLIENT_SECRET')
cognito_client = boto3.client('cognito-idp', region_name=region)
url = os.getenv('URL')


def generate_secret_hash(username):
    """
    Generate the SECRET_HASH required for Cognito.
    """
    message = username + client_id
    dig = hmac.new(
        client_secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode('utf-8')


def sign_up_user(username, email, password, group_name):
    """
    Sign up a user in Cognito and add the user to a group.
    Validate the group name before creating the user.
    """
    # Validate group name
    try:
        cognito_client.get_group(
            GroupName=group_name,
            UserPoolId=os.getenv('USER_POOL_ID')
        )
    except cognito_client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Group '{group_name}' does not exist.")
    secret_hash = generate_secret_hash(username)

    response = cognito_client.sign_up(
        ClientId=client_id,
        SecretHash=secret_hash,
        Username=username,
        Password=password,
        UserAttributes=[
            {
                'Name': 'email',
                'Value': email
            },
        ]
    )
    # Add user to group
    cognito_client.admin_add_user_to_group(
        UserPoolId=os.getenv('USER_POOL_ID'),
        Username=username,
        GroupName=group_name
    )
    return response


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


def get_user_groups(username):
    """
    Get the groups a user belongs to from Cognito.
    """
    try:
        response = cognito_client.admin_list_groups_for_user(
            UserPoolId=os.getenv('USER_POOL_ID'),
            Username=username
        )
        return [group['GroupName'] for group in response['Groups']]

    except Exception as e:
        print(f"Error retrieving groups for user {username}: {e}")
        return None


# API Gateway requests
def get_tasks(id_token, username=""):
    """
    Get tasks from the DynamoDB table using the API Gateway.
    An admin provides no username and can view all tasks,
    while a user provides their username to view only their tasks.
    """
    headers = {'Token': id_token}
    headers['Member'] = username if username else ''
    response = requests.request("GET", url, headers=headers, data={})
    result = sorted(response.json(), key=lambda x: x['id']['N'])
    return result


def create_task(id_token, task_name, task_status, task_assignee, task_deadline):
    """
    Create a task in the DynamoDB table using the API Gateway.
    """
    headers = {'Token': id_token}
    payload = json.dumps({
        'name': task_name,
        'status': task_status,
        'assignee': task_assignee,
        'deadline': task_deadline
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


# def get_user_email(access_token):
#     """
#     Get the user email from Cognito using the access token.
#     """
#     response = cognito_client.get_user(
#         AccessToken=access_token
#     )
#     return response['UserAttributes'][0]['Value']
